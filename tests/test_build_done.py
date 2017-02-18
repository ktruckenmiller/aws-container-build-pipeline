import pytest
import json
from pprint import pprint
def test_emit_events(monkeypatch):
    from builder import build_done

    # both pass
    done_event = [{u'err': u'false', u'image_name': u'ktruckenmiller/docker-friend', u'codebuild_id': u'docker-friend:847fab3c-581b-4b28-b098-246d70af459d', u'tag': u'0.0.50', u'build_started_uuid': u'cb7fd9aa-f19c-11e6-a93d-3afcd3ad5470', u'repo_name': u'docker-friend'}, {u'err': u'false', u'image_name': u'ktruckenmiller/docker-events', u'codebuild_id': u'docker-friend:7917fbac-2948-4329-8d7d-9a7317972055', u'tag': u'0.0.50', u'build_started_uuid': u'cb7fd9aa-f19c-11e6-a93d-3afcd3ad5470', u'repo_name': u'docker-friend'}]
    assert build_done.emit_events(done_event)

    # both failed
    done_event = [{u'codebuild_id': u'docker-friend:edc1c618-7972-48d0-9b22-c1e11cb7fbd2', u'tag': u'0.0.42', u'err': u'true', u'repo_name': u'sadf'}, {u'codebuild_id': u'docker-friend:ec45c630-52f0-4b72-95b4-83a951f42cb2', u'tag': u'0.0.42', u'err': u'true', u'repo_name': u'asdf'}]
    assert build_done.emit_events(done_event) == False

    # one failed, one passed
    done_event = [{u'codebuild_id': u'docker-friend:edc1c618-7972-48d0-9b22-c1e11cb7fbd2', u'tag': u'0.0.42', u'err': u'false', u'repo_name': u'asdf'}, {u'codebuild_id': u'docker-friend:ec45c630-52f0-4b72-95b4-83a951f42cb2', u'tag': u'0.0.42', u'err': u'true', u'repo_name': u'asdf'}]
    assert build_done.emit_events(done_event) == False

def test_build_done_events(monkeypatch):
    from builder.lib import build_events
    monkeypatch.setenv('AWS_DEFAULT_REGION', 'us-west-2')
    monkeypatch.setenv('TABLE_NAME', 'events-table-EventDb-VBTRJR26RPRS')
    event_obj = build_events.BuildEvents()
    builds = [{u'err': u'false', u'image_name': u'ktruckenmiller/docker-friend', u'codebuild_id': u'docker-friend:847fab3c-581b-4b28-b098-246d70af459d', u'tag': u'0.0.50', u'build_started_uuid': u'cb7fd9aa-f19c-11e6-a93d-3afcd3ad5470', u'repo_name': u'docker-friend', u'deploy_id': u'35545b4e-f328-11e6-892e-02a7c0db9301', u'state_machine_arn': u'arn:aws:states:us-west-2:601394826940:stateMachine:build-docker-friend-0_0_52'}]
    pprint(event_obj.send_build_done_event(builds, True))

    # res = event_obj.send_build_completed_event(build, True)
    # print res
