from os import environ
import boto3
import json
from botocore.client import Config
from boto3 import Session

AWS_REGION = environ.get('AWS_REGION')
DEBUG = True

S3_BUCKET = environ.get('S3_BUCKET')
S3_PREFIX = environ.get('S3_PREFIX')

def lambda_handler(event, context):

  s3client = Session().client('s3')

  response = s3client.list_objects(
      Bucket=S3_BUCKET,
      Prefix=S3_PREFIX
  )
  json_str = ''
  cdn_prefix = event.get("cdn_prefix")  or "https://www.maruking.net"
  
  short_url_list = []
  if 'Contents' in response:  # 該当する key がないと response に 'Contents' が含まれない
      keys = [content['Key'] for content in response['Contents']]
      s3 = boto3.client('s3', config=Config(signature_version='s3v4'))
      
      for key in keys:
           resp = s3.head_object(Bucket=S3_BUCKET, Key=key)
           print(resp)
          
           #ここで実際のURLを取得し、CloudFrontへリダイレクトURLを返却
           redirect_url = resp.get('WebsiteRedirectLocation')
           text = resp.get('Metadata').get("comment")
           
           short_url = cdn_prefix + key[1:]
           short_url_dic = short_url, (redirect_url,text)
           short_url_list.append(short_url_dic)
      
  return {
    'statusCode': 200,
    'headers': {
            'Access-Control-Allow-Origin' : '*',
        },
    'body': short_url_list
  }