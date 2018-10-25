import os
import requests


def post_to_slack(event, context):
    slack_webhook_url = os.environ['SLACK_WEBHOOK_URL']

    print(slack_webhook_url)

    ##event is a dictionary - use Glob ** to pass the event

    slack_message = "From {source} at {detail[StartTime]}: {detail[Description]}".format(**event)
    data = {"text": slack_message}

    requests.post(slack_webhook_url, json=data)

    slack_message = "From {source} at {detail[Cause]}".format(**event)
    data = {"text": slack_message}

    requests.post(slack_webhook_url, json=data)


    print(event)

    return


# event example:
# {'version': '0', 'id': '130ba3a5-df64-a7b6-93bc-d49da14e300f', 'detail-type': 'EC2 Instance Launch Successful', 'source': 'aws.autoscaling',
# 'account': '148251350517', 'time': '2018-10-17T19:21:07Z', 'region': 'us-east-1', 'resources':
#  ['arn:aws:autoscaling:us-east-1:148251350517:autoScalingGroup:44be58f7-0b7d-4bd1-a5e6-872d4fbee84f:autoScalingGroupName/Notifon Example Group',
# 'arn:aws:ec2:us-east-1:148251350517:instance/i-0c173e402dcba60b8'], 'detail': {'Description': 'Launching a new EC2 instance: i-0c173e402dcba60b8',
# 'Details': {'Subnet ID': 'subnet-bf858c92', 'Availability Zone': 'us-east-1c'},
# 'EndTime': '2018-10-17T19:21:07.306Z', 'RequestId': '92e59a0d-e3c3-07c4-3753-a3449883ad04',
# 'ActivityId': '92e59a0d-e3c3-07c4-3753-a3449883ad04',
# 'Cause': 'At 2018-10-17T19:20:16Z a user request executed policy Scale Up changing the desired capacity from 1 to 2.  At 2018-10-17T19:20:30Z an instance was started in response to a difference between desired and actual capacity, increasing the capacity from 1 to 2.',
# 'AutoScalingGroupName': 'Notifon Example Group', 'StartTime': '2018-10-17T19:20:33.217Z', 'EC2InstanceId': 'i-0c173e402dcba60b8',
# 'StatusCode': 'InProgress', 'StatusMessage': ''}}