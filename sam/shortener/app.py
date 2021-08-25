import boto3
import os
import random
import string
import botocore
from botocore.client import Config

AWS_REGION = os.environ['AWS_REGION']

DEBUG = True

# generate a random string of n characters, lowercase and numbers
def generate_random(n):
  return ''.join(random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(n))

# checks whether an object already exists in the Amazon S3 bucket
# we do a head_object, if it throws a 404 error then the object does not exist
def exists_s3_key(s3_client, bucket, key):
  try:
    resp = s3_client.head_object(Bucket=bucket, Key=key)
    return True
  except botocore.exceptions.ClientError as e:
    # if ListBucket access is granted, then missing file returns 404
    if (e.response['Error']['Code'] == "404"): return False
    # if ListBucket access is not granted, then missing file returns 403 (which is the case here)
    if (e.response['Error']['Code'] == "403"): return False
    print(e.response)
    raise e     # otherwise re-raise the exception

def handler(event, context):
  print(event)
  BUCKET_NAME = os.environ['S3_BUCKET']   # from env variable

  native_url = event.get("url_long")
  commnet_input = event.get("comment")
  # domain-name
  cdn_prefix = event.get("cdn_prefix") 
