import boto3
import traceback
import os
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
    build_events = build_obj.get_build_events()

    state_machine = step_obj.get_state_machine(build_events)

    sfn = boto3.resource('stepfunctions', region_name=os.environ['AWS_DEFAULT_REGION'])
    state_machine = sfn.create_state_machine(state_machine)

    if state_machine['ResponseMetadata']['HTTPStatusCode'] == 200:
        step_obj.set_state_arn(state_machine['stateMachineArn'])

        # emit build_started with
        event_obj = build_events.BuildEvents()
        event_obj.send_build_started_event(step_obj.builds[0])
        
        # start execution
        step_obj.start_execution(
            stateMachineArn=step_obj.state_machine['stateMachineArn'],
            input=json.dumps({'builds': step_obj.builds})
        )
