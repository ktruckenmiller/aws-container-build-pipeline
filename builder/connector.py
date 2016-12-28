from lib.repository import RepositoryConnector
from credstash import getSecret

def lambda_handler(event, context):
    TOKEN = getSecret('github.token', region=os.environ['AWS_DEFAULT_REGION'])
    print TOKEN






if __name__ == "__main__":
    lambda_handler({}, {})
