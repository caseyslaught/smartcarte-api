import boto3

from SmartCarteApi.common.aws import get_boto_client


def put_object(body, bucket, object_key):
    client = get_boto_client('s3')
    client.put_object(Body=body, Bucket=bucket, Key=object_key)


def put_file(file_path, bucket, object_key):
    s3 = boto3.resource('s3')
    s3.meta.client.upload_file(file_path, bucket, object_key)


