import boto3
import traceback
import os
from lib import build_events

def lambda_handler(event, context):
    try:
        event_obj = build_events.BuildEvents()
        event_obj.send_build_done_event(event)
    except Exception as e:
        print event
        traceback.print_exc()
