import boto3
import json
import traceback
from lib import codebuilder

def lambda_handler(event, context):
    try:
        main(event)

    except Exception as e:
        traceback.print_exc()


def main(event):


    message = event['Records'][0]['Sns']['Message']
    print message


    message = json.loads(message)
    build_obj = codebuilder.CodeBuilder()
    build_obj.parse_github_message(message)

    print message["ref"]
    print message["before"]
    print message["repository"]["id"]
    print message["repository"]["name"]
