from builder import connector
from mock import Mock
import os

def test_connector(monkeypatch):

    cwd = Mock(return_value='/')
    monkeypatch.setenv('ORG_NAME', "ktruckenmiller")
    monkeypatch.setenv('SNS_TOPIC_ARN', "arn:aws:sns:us-west-2:601394826940:GithubEventTopic")
    monkeypatch.setenv('AWS_DEFAULT_REGION', "us-west-2")

    # connector.lambda_handler({
    #     "repo_name": 'node-shairport-metaparser'
    # }, {})

    connector.list_sns()
