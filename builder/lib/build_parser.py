import requests
import credstash
import os
import boto3
import yaml

from pprint import pprint

class BuildParser:

    def __init__(self, record):
        self.date_created = record['date_created']['S']
        self.date_modified = record['date_modified']['S']
        self.id = record['id']['S']
        self.event_type = record['event_type']['S']
        self.logs = record['logs']['S']
        self.repo_id = record['repo_id']['S']
        self.repo_name = record['repo_name']['S']
        self.repo_owner = record['repo_owner']['S']
        self.sha = record['sha']['S']
        self.tag = record['tag']['S']
        self.branch = "master"
        self.build_events = []

        self.possible_types = [
            'dockerhub',
            'ecr',
            's3'
        ]

    def get_om_file(self):
        self.github_token = credstash.getSecret('github.token', region=os.environ['AWS_DEFAULT_REGION'])
        self.github_username = credstash.getSecret('github.username', region=os.environ['AWS_DEFAULT_REGION'])
        url = "https://api.github.com/repos/"+ self.repo_owner +"/" + self.repo_name + "/contents"
        git_files = requests.get(url, headers={'Authorization' : 'token ' + self.github_token}, params={'ref': self.tag}).json()
        file_obj = {}
        pprint(git_files)
        for f in git_files:
            if f['name'] == '.om':
                the_file = requests.get(f['download_url']).text
                file_obj = yaml.load(the_file)
                self.om_file = file_obj
                return self.om_file
        raise Exception('no om file. moving on')

    def parse_single_event(self, event):
        new_event = {
            "tag": self.tag,
            "branch": self.branch,
            "repo_name": self.repo_name,
            "repo_owner": self.repo_owner,
            "repo_id": self.repo_id,
            "sha": self.sha,
            "codebuild_project": self.codebuild_project['arn'],
            "type": self.get_build_type(event),
            "activity_arn": self.get_activity_arn("build-" + self.repo_name + "-" + event['name'])
        }
        return dict(new_event, **event)

    def get_build_type(self, build):
        for index, key in build.iteritems():
            if index in self.possible_types:
                 return index

    def get_activity_arn(self, name):
        stfn = boto3.client('stepfunctions', region_name=os.environ['AWS_DEFAULT_REGION'])
        return stfn.create_activity(name=name)['activityArn']

    def has_codebuild_project(self):
        codebuild = boto3.client('codebuild', region_name=os.environ['AWS_DEFAULT_REGION'])
        self.project = self.repo_name
        if not self.branch == 'master':
            self.project = self.project + '-' + self.branch
        response = codebuild.batch_get_projects(
            names=[
                self.project,
            ]
        )
        for proj in response['projectsNotFound']:
            if proj == self.project:
                return False
        for proj in response['projects']:
            if proj['name'] == self.project:
                self.codebuild_project = proj
                return True
        raise Exception("We can't find the project " + self.project)

    def create_codebuild_project(self):
        codebuild = boto3.client('codebuild', region_name=os.environ['AWS_DEFAULT_REGION'])
        res = codebuild.create_project(
            name=self.project,
            source={
                "auth": {
                    "type": "OAUTH"
                },
                "type": "GITHUB",
                "location": 'https://github.com/'+ self.repo_owner +'/' + self.repo_name + '.git'
            },
            environment={
                "type": "LINUX_CONTAINER",
                "image": "aws/codebuild/docker:1.12.1",
                "computeType": "BUILD_GENERAL1_SMALL"
            },
            serviceRole=os.environ['CODEBUILD_ROLE'],
            artifacts={"type": "NO_ARTIFACTS"},
            timeoutInMinutes=30
        )

        pprint(res)
        if not res['ResponseMetadata']['HTTPStatusCode'] == 200:
            raise Exception("Something's wrong with amazon or their api. " + str(res))
        else:
            self.codebuild_project = res['project']

    def get_build_events(self):
        if not self.has_codebuild_project():
            self.create_codebuild_project()

        all_events = []
        for build in self.om_file['build']['artifacts'].iteritems():

            build[1]['name'] = build[0]
            build = self.parse_single_event(build[1])
            all_events.append(build)

        return all_events
