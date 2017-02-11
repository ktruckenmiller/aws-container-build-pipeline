import requests
import credstash
import os
import boto3
import yaml
import json
from pprint import pprint


class StepBuilder:
    def __init__(self):
        pass
        # https://docs.aws.amazon.com/step-functions/latest/dg/awl-ref-paths.html
        ## 1. run lambda that has these InputPath $.builds[0], $.builds[1]
        #  2. That lambda creates a codebuild job

    def get_build_steps(self, builds):
        self.builds = builds
        steps = []
        for index, build in enumerate(builds):
            step = {
                "StartAt": "codebuild-"+build['name'],
                "States": {
                    "codebuild-"+build['name']: {
                        "Type": "Task",
                        "InputPath": "$.builds[" + str(index) + "]",
                        "Resource": os.environ['BUILD_SPAWN'],
                        "Next": "wait-for-"+build['name']
                    },
                    "wait-for-"+build['name']: {
                        "Type": "Task",
                        "Resource": build['activity_arn'],
                        "End": True
                    }
                }
            }
            steps.append(step)
        return steps

    def build_state_machine(self, events):
        state_machine = {
            "name": "build-" + events[0]["repo_name"] + "-" + events[0]["tag"].replace(".", "_"),
            "roleArn": os.environ["STATE_MACHINE_ROLE"]
        }
        self.state_scaffold = {
            "Comment": "The state machine for the " + "build-" + events[0]["repo_name"] + "-" + events[0]["tag"].replace(".", "_"),
            "StartAt": "BuildState",
            "States": {
                "BuildState": {
                    "Type": "Parallel",
                    "Branches": self.get_build_steps(events),
                    "Next": "BuildCompletedState"
                },
                "BuildCompletedState": {
                    "Type": "Task",
                    "Resource": os.environ["BUILD_DONE_LAMBDA"],
                    "End": True
                }
            }
        }
        state_machine['definition'] = json.dumps(self.state_scaffold)
        return state_machine

    def set_state_arn(self, arn):
        self.state_machine_arn = arn
        new_builds = []
        for build in self.builds:
            build['stateMachineArn'] = arn
            new_builds.append(build)
        self.builds = new_builds
        print self.builds
