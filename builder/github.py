import json
import traceback
from lib import github_events

def lambda_handler(event, context):
    try:
        main(event)

    except Exception as e:
        traceback.print_exc()


def main(event):


    message = event['Records'][0]['Sns']['Message']


    message = json.loads(message)
    build_obj = github_events.GithubEvents()
    build_obj.parse_github_message(message)
    if build_obj.event_type == 'git_tag':
        build_obj.update_event()
    else:
        print "I couldn't parse this event"
        print event
