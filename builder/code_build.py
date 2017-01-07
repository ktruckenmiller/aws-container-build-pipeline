import boto3
import traceback
import os

def lambda_handler(event, context):
    try:
        main(event)

    except Exception as e:
        print event
        traceback.print_exc()


def main(event):

    print "execute code build"
    print event
