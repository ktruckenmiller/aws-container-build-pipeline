from builder import github
from mock import Mock
import os
import json

def open_file(filename):
    with open("tests/testdata/"+filename, 'r') as f:
        read_data = f.read()
        return read_data

def test_simple_build_event(monkeypatch):

    cwd = Mock(return_value='/')
    monkeypatch.setenv('AWS_DEFAULT_REGION', "us-west-2")
    monkeypatch.setenv('TABLE_NAME', '')

    # tag_event = json.loads(open_file("tag.json"))
    # code_obj = github.github_events.GithubEvents()
    # code_obj.parse_github_message(tag_event)
