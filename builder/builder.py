import boto3
import traceback

def lambda_handler(event, context):
    try:
        main(event)
    except Exception as e:
        traceback.print_exc()


def main(event):
    print event

# parse build events

# process build events
    # check if the right Type
    # create/update a codebuild job based on the definition

#
