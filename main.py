import requests
import boto3
from botocore import UNSIGNED
from botocore.client import Config

s3 = boto3.client('s3')

bucket_name = 'coderbytechallengesandbox'
prefix = '__cb__'
s3 = boto3.resource('s3', config=Config(signature_version=UNSIGNED))
bucket = s3.Bucket(bucket_name)
objects = bucket.objects.filter(Prefix='__cb__')
for object in objects:
    print(object.key)
