import boto3
import traceback
import os
import yaml
import json
from pprint import pprint
from lib import build_parser, step_builder


def lambda_handler(event, context):
    try:
        main(event)

    except Exception as e:
        print event
        traceback.print_exc()


def main(event):
    pprint(event)
    ## Run codebuild job
    ## TODO: env varible overrides need to be dynamic  or image name
    codebuild = boto3.client('codebuild', region_name=os.environ['AWS_DEFAULT_REGION'])
    res = codebuild.start_build(
        projectName=event['repo_name'],
        sourceVersion=event['sha'],
        environmentVariablesOverride=[{
                    "name": "ACTIVITY_ARN",
                    "value": event['activity_arn']
                },{
                    "name": "DOCKERFILE_LOCATION",
                    "value": event['dockerfile']
                },{
                    "name": "ORG_NAME",
                    "value": event['repo_owner']
                },{
                    "name": "REPO_NAME",
                    "value": event['repo_name']
                },{
                    "name": "STATE_MACHINE_ARN",
                    "value": event['stateMachineArn']
                },{
                    "name": "IMAGE_NAME",
                    "value": event['dockerhub']
                },{
                    "name": "DEPLOY_ID", ##should be state_id
                    "value": event['id']
                },{
                    "name": "TAG",
                    "value": event['tag']
                }],
        buildspecOverride=get_buildspec_template(event['type'])
    )
    print res

def get_buildspec_template(build_type):
    templates = {
        'dockerhub': 'dockerhub_buildspec.yml'
    }
    current_dir = os.path.dirname(os.path.realpath(__file__))
    return open_file(os.path.dirname(os.path.realpath(__file__)) + "/templates/" + templates[build_type])
    ## emit build_running event

def open_file(filename):
    with open(filename, 'r') as f:
        read_data = f.read()
        read_data = yaml.load(read_data)
        return json.dumps(read_data)
