from builder import github
from mock import Mock
import os
import json

def open_file(filename):
    with open("tests/testdata/"+filename, 'r') as f:
        read_data = f.read()
        return read_data

def test_github_events_tag(monkeypatch):

    cwd = Mock(return_value='/')
    monkeypatch.setenv('AWS_DEFAULT_REGION', "us-west-2")
    monkeypatch.setenv('TABLE_NAME', 'events-table-EventsTable-1DEO4ALJ6IORA')

    tag_event = json.loads(open_file("tag.json"))
    code_obj = github.github_events.GithubEvents()
    code_obj.parse_github_message(tag_event)


def test_github_events_commit(monkeypatch):
    cwd = Mock(return_value='/')
    monkeypatch.setenv('AWS_DEFAULT_REGION', "us-west-2")
    monkeypatch.setenv('TABLE_NAME', "us-west-2")

    commit_event = json.loads(open_file("commit.json"))
    code_obj = github.github_events.GithubEvents()
    boston = code_obj.parse_github_message(commit_event)
    print boston
