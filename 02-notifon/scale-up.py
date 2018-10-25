import boto3
session = boto3.Session(profile_name='local-machine')
as_client = session.client('autoscaling')

# console.aws: EC2 -> Auto Scaling Groups
as_client.execute_policy(AutoScalingGroupName='Notifon Example Group', PolicyName='Scale Up')
