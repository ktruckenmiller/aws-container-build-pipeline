import boto3
import os
import uuid
import json
from pprint import pprint
from datetime import datetime
from credstash import getSecret
ISO_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"


class BuildEvents:
    def __init__(self):
        dynamodb = boto3.resource('dynamodb', region_name=os.environ['AWS_DEFAULT_REGION'])
        self.events_table = dynamodb.Table(os.environ['TABLE_NAME'])
        self.uuid = uuid.uuid1()

    def send_build_started_event(self, event, testing=False):
        newItem = {
            "id": str(self.uuid),
            "event_type": "build_started",
            "sha": event['sha'],
            "tag": event['tag'],
            "repo_name": event['repo_name'],
            "repo_owner": event['repo_owner'],
            "repo_id": event['repo_id'],
            "logs": json.dumps({'state_machine_arn': event['stateMachineArn']}),
            "date_created": datetime.utcnow().strftime(ISO_FORMAT),
            "date_modified": datetime.utcnow().strftime(ISO_FORMAT)
        }
        # if not testing:
        res = self.events_table.put_item(
            Item=newItem
        )
        print(json.dumps(res, indent=4))

    def send_build_done_event(self, event, testing=False):
        # print 'send build failed event'
        # print event

        build_type = "build_completed"
        for build in event:
            if build['err'] == 'true':
                build_type = "build_failed"

        # get related event from id
        build_relative_event = self.events_table.get_item(
            Key={
                'id': event[0]['deploy_id']
            }
        )['Item']
        newItem = {
            "id": str(self.uuid),
            "event_type": build_type,
            "sha": build_relative_event['sha'],
            "tag": build_relative_event['tag'],
            "repo_name": build_relative_event['repo_name'],
            "repo_owner": build_relative_event['repo_owner'],
            "repo_id": build_relative_event['repo_id'],
            "date_created": datetime.utcnow().strftime(ISO_FORMAT),
            "payload": json.dumps({
                "state_machine_arn": event[0]['state_machine_arn'],
                "codebuild_id": event[0]['codebuild_id'],
                "builds": event
            }),
            "date_modified": datetime.utcnow().strftime(ISO_FORMAT)
        }

        if not testing:
            res = self.events_table.put_item(
                Item=newItem
            )
        else:
            return newItem
