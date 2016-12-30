from lib.repository import RepositoryConnector


def lambda_handler(event, context):
    if 'repo_name' in event:
        potential_repo = RepositoryConnector(event['repo_name'])
        if potential_repo.has_repo():
            potential_repo.create_hook()
        else:
            print "No repo of that name, or somethings wrong with that."

    else:
        print event
        print "no repo name in event"

def list_sns():
    potential_repo = RepositoryConnector('node-shairport-metaparser')
    print potential_repo.list_sns()
