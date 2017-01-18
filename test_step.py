import boto3
import json
from pprint import pprint
client = boto3.client('stepfunctions')

def main():
    ### ALL GOOD
    # state_machine = create_state()
    # state_machine = {
    #     'stateMachineArn': 'arn:aws:states:us-west-2:601394826940:stateMachine:test-state-machine'
    # }
    # execution = start_it_up(state_machine['stateMachineArn'])
    # print execution

    #activity arn? arn:aws:states:us-west-2:601394826940:activity:test-codebuild
    # response = client.send_task_success(
    #     taskToken='AAAAKgAAAAIAAAAAAAAAAfSlxPL2bIkJ++/BnslpfGKshH00cLk+AWvSdlwylMn/TWhX5yCrjbF8aXeoK8fg4US+JYGviO4q8hg/T3mrpdNPPCM8lr2eq3sxXK6o9cqEaPZ1OZ1vszkL8LolyCa7sMB1Am1EZXioufkb4TkMHx3H7aq0tGFrNug3RzFXRfu7M+fBX9F1wEihh6oUtx2ECrk+nGWJTLruioUehR7U0QktpsH1Caq9EfWSWHNp9aQ4mI78/eeRsJIo9A7vZqM1MX68mttYbmbTWTjiEnw+lNYUtS70kL9o9a/SMybY6VAJNoqf0omnOa7T2V+ygC5TAtEOf8U3oPvH523elQ0Ur6OoSb8gB48MLi23nyq729ePE2BHoGkI+p/EpMpMroz117vGkWATXGma6ALFzG49ZTu4xdJKDhrMbFQY5Xm+hxdhw8CDj6Vc6o/JqExg75z4Qq6jDFZEEe2QV42CaE8KK8peM0tIH0rPYiNxI0g+5becE+1K1PhbbKUdB0YFPYsmUtwz3JFXJvrG1djBIwoBKi4=',
    #     output='{\"boston\": \"shoey\"}'
    # )
    # print response

def start_it_up(state_machine):
    test_obj = {
        "boston": "shoey"
    }
    response = client.start_execution(
        stateMachineArn=state_machine,
        name='some-name-for-execution',
        input=str(json.dumps(test_obj))
    )
    return response

def create_state():
    stuff = openJson()
    stuff = json.dumps(stuff)

    return client.create_state_machine(
        name="test-state-machine",
        definition=str(stuff),
        roleArn="arn:aws:iam::601394826940:role/service-role/StatesExecutionRole-us-west-2"
    )

def openJson():
    #new
    try:
        with open('test_step_function.json') as data_file:
            testobj = json.load(data_file)
            return testobj
    except Exception as e:
        print "File open error. Parsing json or file opening error"

if __name__ == "__main__":
    main()
