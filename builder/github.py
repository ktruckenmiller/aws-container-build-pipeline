import boto3
import json

def lambda_handler(event, context):
    try:
        main(event)

    except Exception as e:
        print str(e)


def main(event):
    message = event['Records'][0]['Sns']['Message']
    print message
