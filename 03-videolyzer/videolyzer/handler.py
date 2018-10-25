import urllib
import boto3
import os
import json

def start_label_detection(bucket, key):
   rekognition_client = boto3.client('rekognition')

   response = rekognition_client.start_label_detection(
      Video = {
         'S3Object': {
            'Bucket': bucket,
            'Name': key
         }
      },
      NotificationChannel = {
         'SNSTopicArn': os.environ['REKOGNITION_SNS_TOPIC_ARN'],
         'RoleArn': os.environ['REKOGNITION_ROLE_ARN']
      }
   )

   print(response)

   return

def get_video_labels(job_id):

   rekognition_client = boto3.client('rekognition')

   response = rekognition_client.get_label_detection(JobId=job_id)

   next_token = response.get('NextToken', None)

   while next_token:
      next_page = rekognition_client.get_label_detection(JobId=job_id, NextToken=next_token)

      response['Labels'].extend(next_page['Labels'])

      next_token = next_page.get('NextToken', None)

   print(response['Labels'])

   return response


def make_item(data):
   if isinstance(data, dict):
      # for k, v in data.items():
      #    print("{0} - {1}".format(k, v))

      return {k: make_item(v) for k, v in data.items()}

   if isinstance(data, list):
      return [ make_item(v) for v in data ]

   if isinstance(data, float):
      return str(data)

def put_labels_in_db(data, video_name, video_bucket):

   del data['ResponseMetadata']
   del data['JobStatus']

   dynamodb = boto3.resource('dynamodb')
   videos_table = dynamodb.Table(os.environ['DYNAMODB_TABLE_NAME'])

   data = make_item(data)
   data['videoName'] = video_name
   data['videoBucket'] = video_bucket

   print(data['videoName'])
   print(data['videoBucket'])

   videos_table.put_item(Item=data)

   return


## Lambda Events:

def start_processing_video(event, context):

   print(len(event['Records']))
   for record in event['Records']:
      bucket_name = record['s3']['bucket']['name']
      record_key = urllib.parse.unquote_plus(record['s3']['object']['key'])

      start_label_detection(bucket_name, record_key)

   return

def handle_label_detection(event, context):

   for record in event['Records']:
      message = json.loads(record['Sns']['Message'])

      job_id = message['JobId']
      s3_object = message['Video']['S3ObjectName']
      s3_bucket = message['Video']['S3Bucket']

      print("JobId {JobId} - Video Name: {Video[S3ObjectName]}: Bucket: {Video[S3Bucket]}".format(**message))

      response = get_video_labels(job_id)

      put_labels_in_db(response, s3_object, s3_bucket)

   return


