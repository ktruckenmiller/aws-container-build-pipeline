import boto3
import os
from credstash import getSecret

class CodeBuilder:
    def __init__(self):
        self.github_token = self.get_cred('github.token')
        self.github_aws_key = self.get_cred('github.aws.key')
        self.github_aws_secret = self.get_cred('github.aws.secret')
        self.region = os.environ['AWS_DEFAULT_REGION']


    def set_owner(self, owner):
        self.owner = owner


    def parse_github_message(self, message):
        self.repository = message["repository"]["name"]
        self.tag = self.get_tag(message['ref'])
        self.sha = message["head_commit"]["id"]

        print message["ref"]
        print message["before"]
        print message["repository"]["id"]
        print

    def get_cred(self, cred):
        return getSecret(cred, region=os.environ['AWS_DEFAULT_REGION'])

    def get_tag(self, ref):
        if 'refs/tags' in ref:
            return ref.split("refs/tags/")[1]
