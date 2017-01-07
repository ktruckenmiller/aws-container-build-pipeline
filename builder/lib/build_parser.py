import requests
import credstash
import os
import yaml

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

    def get_om_file(self):
        github_token = credstash.getSecret('github.token', region=os.environ['AWS_DEFAULT_REGION'])
        url = "https://api.github.com/repos/"+ self.repo_owner +"/" + self.repo_name + "/contents"
        git_files = requests.get(url, headers={'Authorization' : 'token ' + github_token}, params={'ref': self.tag}).json()
        file_obj = {}
        for file in git_files:
            if file['name'] == '.om':
                the_file = requests.get(file['download_url']).text
                file_obj = yaml.load(the_file)
                self.om_file = file_obj
                return self.om_file

    def parse_single_event(self, event):
        new_event = {
            "tag": self.tag,
            "branch": self.branch,
            "repo_name": self.repo_name,
            "repo_owner": self.repo_owner,
            "repo_id": self.repo_id,
            "sha": self.sha
        }
        return dict(new_event, **event)

    def get_build_events(self):
        all_events = []
        for event in self.om_file['build']['artifacts'].iteritems():
            event[1]['name'] = event[0]
            event = self.parse_single_event(event[1])
            all_events.append(event)

        return all_events
