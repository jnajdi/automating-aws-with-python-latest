# coding: utf-8
import boto
import boto3
session = boto3.Session(profile_name='local-machine')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='videolyzer-videos')
from pathlib import Path
get_ipython().run_line_magic('ls', '*')
pathname='/Users/jihane/Development/sandbox/automating-aws-with-python/Blurred_Bokeh_Video.mp4'
print(path)
print(pathname)
path = Path(pathname).expanduser().resolve()
print(path)
bucket.upload_file(str(path), str(path.name))
rekognition_client = session.client('rekognition')
responce = rekognition_client.start_label_detection(Video={'S3Object':{'Bucket': bucket.name, 'Name': path.name}})
responce
responce.job_id
job_id = responce[job_id]
job_id = responce['JobId']
job_id
result = rekognition_client.get_label_detection(JobId=job_id)
result
result.keys()
result['JobStatus']
result['VideoMetadata']
result['Labels']
