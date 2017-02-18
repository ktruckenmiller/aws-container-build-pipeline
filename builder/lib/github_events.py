import boto3
import os
import uuid
import json
from datetime import datetime
from credstash import getSecret
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class GithubEvents:
    git_types = [
        'git_tag',
        'git_commit'
    ]
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_DEFAULT_REGION'])
        self.events_table = dynamodb.Table(os.environ['TABLE_NAME'])
        self.github_token = self.get_cred('github.token')
        self.github_aws_key = self.get_cred('github.aws.key')
        self.github_aws_secret = self.get_cred('github.aws.secret')
        self.region = os.environ['AWS_DEFAULT_REGION']
        self.uuid = uuid.uuid1()

    def set_owner(self, owner):
        self.owner = owner


    def parse_github_message(self, message):
        self.repo_name = message["repository"]["name"]
        self.repo_id = message["repository"]["id"]
        self.tag = self.get_tag(message['ref'])
        self.sha = message["head_commit"]["id"]
        self.payload = message
        self.event_type = self.get_type()
        self.repo_owner = message["repository"]["owner"]["name"]


    def get_cred(self, cred):
        return getSecret(cred, region=os.environ['AWS_DEFAULT_REGION'])

    def get_tag(self, ref):
        if 'refs/tags' in ref:
            return ref.split("refs/tags/")[1]

    def get_type(self):
        if self.tag:
            return 'git_tag'
        else:
            print "Non-evented thing"
            print self.payload

    def update_event(self):
        newItem = {
            "id": str(self.uuid),
            "sha": self.sha,
            "tag": self.tag,
            "event_type": self.event_type,
            "repo_name": self.repo_name,
            "repo_owner": self.repo_owner,
            "repo_id": str(self.repo_id),
            "state_id": str(uuid.uuid1())
            "payload": json.dumps(self.payload),
            "date_created": datetime.utcnow().strftime(ISO_FORMAT),
            "date_modified": datetime.utcnow().strftime(ISO_FORMAT)
        }
        res = self.events_table.put_item(
            Item=newItem
        )


        # print(json.dumps(res, indent=4)
