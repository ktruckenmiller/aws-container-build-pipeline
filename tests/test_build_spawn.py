
from mock import Mock
import os
import boto3
import json
import yaml
import pytest
from pprint import pprint


def test_spawn_codebuild(monkeypatch):
    monkeypatch.setenv('AWS_DEFAULT_REGION', "us-west-2")
    monkeypatch.setenv('TABLE_NAME', 'events-table-EventDb-VBTRJR26RPRS')
    monkeypatch.setenv('CODEBUILD_ROLE', 'arn:aws:iam::601394826940:role/build-roles-CodebuildRole-NPDFVGZ929FA')
    monkeypatch.setenv('STATE_MACHINE_ROLE', 'arn:aws:iam::601394826940:role/build-roles-StateMachineRole-1O9DLEQQN7THT')
    monkeypatch.setenv('BUILD_DONE_LAMBDA', 'arn:aws:lambda:us-west-2:601394826940:function:build-lambdas-BuildDone-3WD6IR0D4SLI')
    monkeypatch.setenv('BUILD_SPAWN', 'arn:aws:lambda:us-west-2:601394826940:function:build-lambdas-BuildSpawn-170EI1MOJL59K')

    from builder import build_spawn

    build_obj = {u'repo_id': u'75007036', u'name': u'events', u'dockerhub': u'ktruckenmiller/docker-events', u'type': u'dockerhub', u'repo_owner': u'ktruckenmiller', u'stateMachineArn': u'arn:aws:states:us-west-2:601394826940:stateMachine:build-docker-friend-0.0.21', u'sha': u'aec93480363d97357b3063c77ab51ce4a4ef7047', u'codebuild_project': u'arn:aws:codebuild:us-west-2:601394826940:project/docker-friend', u'tag': u'0.0.21', u'branch': u'master', u'activity_arn': u'arn:aws:states:us-west-2:601394826940:activity:build-docker-friend-events', u'dockerfile': u'Dockerfile.node', u'repo_name': u'docker-friend'}
    build_spawn.lambda_handler(build_obj, {})

def test_get_buildspec_template(monkeypatch):
    from builder import build_spawn
    print build_spawn.get_buildspec_template('dockerhub')


def test_templates(monkeypatch):
    templates = [
        'dockerhub_buildspec.yml'
    ]
    for template in templates:
        open_file(template)

def open_file(filename):
    with open('../builder/templates/'+filename, 'r') as f:
        read_data = f.read()
        read_data = yaml.load(read_data)
        json.dumps(read_data)
