import requests
import json
import os
from credstash import getSecret

class RepositoryConnector:
    def __init__(self, repo_name):
        self.org = os.environ['ORG_NAME']
        self.repo_name = repo_name
        self.github_token = self.get_cred('github.token')
        self.github_aws_key = self.get_cred('github.aws.key')
        self.github_aws_secret = self.get_cred('github.aws.secret')
        self.sns_topic = os.environ['SNS_TOPIC_ARN']
        self.region = os.environ['AWS_DEFAULT_REGION']

    def has_repo(self):
        url = "https://api.github.com/repos/" + self.org + "/" + self.repo_name
        print url
        json_res = requests.get(url, headers={'Authorization' : 'token ' + self.github_token}).json()
        print json_res
        if 'name' in json_res:
            return True
        return False

    def create_hook(self):
        url = "https://api.github.com/repos/" + self.org + "/" + self.repo_name + "/hooks"

        default_sns = {
            'name': 'amazonsns',
            'events': ['push'],
            'config': {
                'aws_secret': self.github_aws_secret,
                'aws_key': self.github_aws_key,
                'sns_topic': self.sns_topic,
                'sns_region': self.region
            },
            'active': True
        }
        json_res = requests.post(url, headers={
            'content-type': 'application/json',
            'Authorization': 'token ' + self.github_token
        }, data=json.dumps(default_sns)).json()

        return json_res

    def test_sns(self, service_id):
        url = "https://api.github.com/repos/" + self.org + "/" + self.repo_name + "/hooks/"+ str(service_id) + "/tests"
        json_res = requests.post(url, headers={
            'content-type': 'application/json',
            'Authorization': 'token ' + self.github_token
        }).text
        return json_res

    def list_sns(self):
        url = "https://api.github.com/repos/" + self.org + "/" + self.repo_name + "/hooks"
        json_res = requests.get(url, headers={'Authorization' : 'token ' + self.github_token}).json()

        return json_res

    def get_cred(self, cred):
        return getSecret(cred, region=os.environ['AWS_DEFAULT_REGION'])
