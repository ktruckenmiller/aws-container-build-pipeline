import boto3
import json
import traceback

def lambda_handler(event, context):
    try:
        main(event)

    except Exception as e:
        traceback.print_exc()


def main(event):
    message = event['Records'][0]['Sns']['Message']
    message = json.loads(message)

    print message["ref"]
    print message["before"]
    print message["repository"]["id"]
    print message["repository"]["name"]
