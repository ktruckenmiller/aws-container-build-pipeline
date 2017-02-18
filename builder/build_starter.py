import boto3
import traceback
import os
import json
from pprint import pprint
from lib import build_parser, step_builder, build_events


def lambda_handler(event, context):
    try:
        record = event['Records'][0]['dynamodb']['NewImage']
        print event
        if record['event_type']['S'] == 'git_tag':
            main(record)

    except Exception as e:
        traceback.print_exc()
        print event
        return {
            "err": True,
            "msg": str(e)
        }



def main(record):

    build_obj = build_parser.BuildParser(record)
    step_obj = step_builder.StepBuilder()

    om_file = build_obj.get_om_file()
    build_steps = build_obj.get_build_steps()

    state_machine = step_obj.build_state_machine(build_steps)
    print(state_machine)
    sfn = boto3.client('stepfunctions', region_name=os.environ['AWS_DEFAULT_REGION'])

    state_machine = sfn.create_state_machine(
        name=state_machine['name'],
        roleArn=state_machine['roleArn'],
        definition=state_machine['definition']
    )

    if state_machine['ResponseMetadata']['HTTPStatusCode'] == 200:
        step_obj.set_state_arn(state_machine['stateMachineArn'])

        # emit build_started with
        event_obj = build_events.BuildEvents()
        event_obj.send_build_started_event(step_obj.builds[0])
        
        # start execution
        sfn.start_execution(
            stateMachineArn=state_machine['stateMachineArn'],
            input=json.dumps({'builds': step_obj.builds})
        )
