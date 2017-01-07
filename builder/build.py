import boto3
import traceback
import os
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
    om_file = build_obj.get_om_file()

    build_events = build_obj.get_build_events()
    print build_events
    # build step function with the code_builder executor?

# creates a step function that outlines the build event, emit a build_started
# event with the step function id in the payload section

# create another lambda that gets triggered at the end of every dynamic
# step function that both cleans up the step function, and emits an event
# build_completed

# if something fails have a lambda that cleans up the step function and emits
# build_failed
