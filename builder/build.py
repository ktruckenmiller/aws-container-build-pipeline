import boto3
import traceback
from lib import build_parser

def lambda_handler(event, context):
    try:
        record = event['Records'][0]['dynamodb']['NewImage']

        if record['event_type']['S'] == 'git_tag':
            main(record)

    except Exception as e:
        print event
        traceback.print_exc()


def main(record):
    build_obj = build_parser.BuildParser(record)
    dir(build_obj)

# parse build events
    # create parent event
    # create child events
    '''
    parent:
        id:
        event_type: build_parent
        children:
            - id:
              done: False
              order: 0
            - id:
              done: False
              order: 1
    child1:
        id:

    '''

# process build events
    # check if the right Type

    # create/update a codebuild job based on the definition

#
