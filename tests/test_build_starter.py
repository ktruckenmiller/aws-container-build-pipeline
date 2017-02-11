from mock import Mock
import os
import boto3
import json
import pytest
from pprint import pprint

def open_file(filename):
    with open("testdata/"+filename, 'r') as f:
        read_data = f.read()
        return read_data

def test_simple_build_event(monkeypatch):

    monkeypatch.setenv('AWS_DEFAULT_REGION', "us-west-2")
    monkeypatch.setenv('TABLE_NAME', 'events-table-EventDb-VBTRJR26RPRS')
    monkeypatch.setenv('CODEBUILD_ROLE', 'arn:aws:iam::601394826940:role/build-roles-CodebuildRole-NPDFVGZ929FA')
    monkeypatch.setenv('STATE_MACHINE_ROLE', 'arn:aws:iam::601394826940:role/build-roles-StateMachineRole-1O9DLEQQN7THT')
    monkeypatch.setenv('BUILD_DONE_LAMBDA', 'arn:aws:lambda:us-west-2:601394826940:function:build-lambdas-BuildDone-3WD6IR0D4SLI')
    monkeypatch.setenv('BUILD_SPAWN', 'arn:aws:lambda:us-west-2:601394826940:function:build-lambdas-BuildSpawn-170EI1MOJL59K')

    from builder.lib import build_parser, step_builder, build_events

    dynamo_event = json.dumps({u'Records': [{u'eventID': u'f6886a3e8033f97cd1f3fce4e9de7df8', u'eventVersion': u'1.1', u'dynamodb': {u'SequenceNumber': u'50720400000000001017486058', u'Keys': {u'id': {u'S': u'63035d40-db5b-11e6-a72e-26971901fb17'}}, u'SizeBytes': 6698, u'NewImage': {u'repo_id': {u'S': u'75007036'}, u'event_type': {u'S': u'git_tag'}, u'date_modified': {u'S': u'2017-01-15T19:47:03.105223Z'}, u'repo_owner': {u'S': u'ktruckenmiller'}, u'logs': {u'S': u'{"forced": false, "compare": "https://github.com/ktruckenmiller/docker-friend/compare/0.0.21", "pusher": {"name": "ktruckenmiller", "email": "kmtruckenmiller@gmail.com"}, "sender": {"following_url": "https://api.github.com/users/ktruckenmiller/following{/other_user}", "events_url": "https://api.github.com/users/ktruckenmiller/events{/privacy}", "organizations_url": "https://api.github.com/users/ktruckenmiller/orgs", "url": "https://api.github.com/users/ktruckenmiller", "gists_url": "https://api.github.com/users/ktruckenmiller/gists{/gist_id}", "html_url": "https://github.com/ktruckenmiller", "subscriptions_url": "https://api.github.com/users/ktruckenmiller/subscriptions", "avatar_url": "https://avatars.githubusercontent.com/u/1864889?v=3", "repos_url": "https://api.github.com/users/ktruckenmiller/repos", "received_events_url": "https://api.github.com/users/ktruckenmiller/received_events", "gravatar_id": "", "starred_url": "https://api.github.com/users/ktruckenmiller/starred{/owner}{/repo}", "site_admin": false, "login": "ktruckenmiller", "type": "User", "id": 1864889, "followers_url": "https://api.github.com/users/ktruckenmiller/followers"}, "repository": {"issues_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/issues{/number}", "deployments_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/deployments", "stargazers_count": 0, "forks_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/forks", "mirror_url": null, "subscription_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/subscription", "notifications_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/notifications{?since,all,participating}", "collaborators_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/collaborators{/collaborator}", "updated_at": "2016-11-28T19:30:23Z", "private": false, "pulls_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/pulls{/number}", "issue_comment_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/issues/comments{/number}", "labels_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/labels{/name}", "has_wiki": true, "full_name": "ktruckenmiller/docker-friend", "owner": {"name": "ktruckenmiller", "email": "kmtruckenmiller@gmail.com"}, "statuses_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/statuses/{sha}", "id": 75007036, "keys_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/keys{/key_id}", "description": "A Docker UI that helps you manage and use containers for local development", "tags_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/tags", "downloads_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/downloads", "assignees_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/assignees{/user}", "contents_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/contents/{+path}", "has_pages": false, "git_refs_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/git/refs{/sha}", "open_issues_count": 0, "clone_url": "https://github.com/ktruckenmiller/docker-friend.git", "watchers_count": 0, "git_tags_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/git/tags{/sha}", "milestones_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/milestones{/number}", "languages_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/languages", "size": 1038, "homepage": null, "fork": false, "commits_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/commits{/sha}", "releases_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/releases{/id}", "issue_events_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/issues/events{/number}", "archive_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/{archive_format}{/ref}", "comments_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/comments{/number}", "events_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/events", "contributors_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/contributors", "html_url": "https://github.com/ktruckenmiller/docker-friend", "forks": 1, "compare_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/compare/{base}...{head}", "open_issues": 0, "git_url": "git://github.com/ktruckenmiller/docker-friend.git", "svn_url": "https://github.com/ktruckenmiller/docker-friend", "merges_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/merges", "has_issues": true, "ssh_url": "git@github.com:ktruckenmiller/docker-friend.git", "blobs_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/git/blobs{/sha}", "master_branch": "master", "git_commits_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/git/commits{/sha}", "hooks_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/hooks", "has_downloads": true, "watchers": 0, "name": "docker-friend", "language": "JavaScript", "url": "https://github.com/ktruckenmiller/docker-friend", "stargazers": 0, "created_at": 1480361376, "pushed_at": 1484509620, "forks_count": 1, "default_branch": "master", "teams_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/teams", "trees_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/git/trees{/sha}", "branches_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/branches{/branch}", "subscribers_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/subscribers", "stargazers_url": "https://api.github.com/repos/ktruckenmiller/docker-friend/stargazers"}, "created": true, "deleted": false, "commits": [], "after": "aec93480363d97357b3063c77ab51ce4a4ef7047", "head_commit": {"committer": {"name": "Kevin Truckenmiller", "email": "kevintruckenmiller@Kevins-MacBook-Pro.local"}, "added": [], "author": {"name": "Kevin Truckenmiller", "email": "kevintruckenmiller@Kevins-MacBook-Pro.local"}, "distinct": true, "timestamp": "2017-01-15T13:46:46-06:00", "modified": ["buildspec.yml"], "url": "https://github.com/ktruckenmiller/docker-friend/commit/aec93480363d97357b3063c77ab51ce4a4ef7047", "tree_id": "2e9d7320428c92d2c10c573336c0bc5a2b985c1f", "message": "updated", "removed": [], "id": "aec93480363d97357b3063c77ab51ce4a4ef7047"}, "ref": "refs/tags/0.0.21", "base_ref": "refs/heads/master", "before": "0000000000000000000000000000000000000000"}'}, u'sha': {u'S': u'aec93480363d97357b3063c77ab51ce4a4ef7047'}, u'tag': {u'S': u'0.0.21'}, u'date_created': {u'S': u'2017-01-15T19:47:03.105206Z'}, u'id': {u'S': u'63035d40-db5b-11e6-a72e-26971901fb17'}, u'repo_name': {u'S': u'docker-friend'}}, u'ApproximateCreationDateTime': 1484509620.0, u'StreamViewType': u'NEW_IMAGE'}, u'awsRegion': u'us-west-2', u'eventName': u'INSERT', u'eventSourceARN': u'arn:aws:dynamodb:us-west-2:601394826940:table/events-table-EventDb-VBTRJR26RPRS/stream/2017-01-05T01:41:53.755', u'eventSource': u'aws:dynamodb'}]})
    dynamo_event = json.loads(open_file('dynamo_event.json'))
    # regression tests
    record = dynamo_event['Records'][0]['dynamodb']['NewImage']
    assert record['event_type']['S'] == 'git_tag'

    build_obj = build_parser.BuildParser(record)
    step_obj = step_builder.StepBuilder()

    build_obj.get_om_file()

    assert build_obj.event_type == 'git_tag'

    all_build_events = build_obj.get_build_events()

    assert all_build_events[1]['codebuild_project'] == "arn:aws:codebuild:us-west-2:601394826940:project/docker-friend"

    state_machine = step_obj.build_state_machine(all_build_events)
    assert state_machine['name'] == 'build-docker-friend-0_0_21'


    sfn = boto3.client('stepfunctions', region_name=os.environ['AWS_DEFAULT_REGION'])
    def mockreturn(name, roleArn, definition):
        return {'ResponseMetadata': {
            'HTTPStatusCode': 200
        }}
    # monkeypatch.setattr(sfn, 'create_state_machine', mockreturn)
    state_machine = sfn.create_state_machine(
        name=state_machine['name'],
        roleArn=state_machine['roleArn'],
        definition=state_machine['definition']
    )
    assert state_machine['ResponseMetadata']['HTTPStatusCode'] == 200
    step_obj.set_state_arn(state_machine['stateMachineArn'])


    event_obj = build_events.BuildEvents()
    event_obj.send_build_started_event(step_obj.builds[0])

    # start execution
    res = sfn.start_execution(
        stateMachineArn=state_machine['stateMachineArn'],
        input=json.dumps({'builds': step_obj.builds})
    )
    pprint(res)

# def test_emit_build_event(monkeypatch):
#     monkeypatch.setenv('AWS_DEFAULT_REGION', "us-west-2")
#     monkeypatch.setenv('TABLE_NAME', 'events-table-EventDb-VBTRJR26RPRS')
#     build = {'repo_id': u'75007036', 'name': 'events', 'dockerhub': 'ktruckenmiller/docker-events', 'dockerfile': 'Dockerfile.node', 'repo_owner': u'ktruckenmiller', 'stateMachineArn': u'arn:aws:states:us-west-2:601394826940:stateMachine:build-docker-friend-0.0.21', 'sha': u'aec93480363d97357b3063c77ab51ce4a4ef7047', 'codebuild_project': {u'name': u'docker-friend', u'serviceRole': u'arn:aws:iam::601394826940:role/codebuild-test-CodebuildRole-1UPIE93C57435', u'tags': [], u'artifacts': {u'type': u'NO_ARTIFACTS'}, u'lastModified': u'j', u'timeoutInMinutes': 30, u'created': u's', u'environment': {u'computeType': u'BUILD_GENERAL1_SMALL', u'image': u'aws/codebuild/docker:1.12.1', u'type': u'LINUX_CONTAINER', u'environmentVariables': []}, u'source': {u'type': u'GITHUB', u'location': u'https://github.com/ktruckenmiller/docker-friend.git', u'auth': {u'type': u'OAUTH'}}, u'encryptionKey': u'arn:aws:kms:us-west-2:601394826940:alias/aws/s3', u'arn': u'arn:aws:codebuild:us-west-2:601394826940:project/docker-friend'}, 'tag': u'0.0.21', 'branch': 'master', 'activity_arn': u'arn:aws:states:us-west-2:601394826940:activity:build-docker-friend-events', 'type': 'dockerhub', 'repo_name': u'docker-friend'}
#     from builder.lib import build_events
#     event_obj = build_events.BuildEvents()
#     event_obj.send_build_started_event(build, True)

# def test_build_spawn(monkeypatch):
