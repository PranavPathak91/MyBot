import boto3
import os
from botocore.exceptions import ClientError

class S3Client:
    def __init__(self):
        self.s3 = boto3.client(
            's3',
            aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
            aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
            region_name=os.getenv('AWS_REGION', 'us-east-1')
        )
        self.bucket = os.getenv('S3_BUCKET_NAME')

    def upload_file(self, file_obj, file_name):
        try:
            self.s3.upload_fileobj(file_obj, self.bucket, file_name)
            return True
        except ClientError as e:
            print(f"Error uploading file to S3: {e}")
            return False

    def get_file(self, file_name):
        try:
            response = self.s3.get_object(Bucket=self.bucket, Key=file_name)
            return response['Body']
        except ClientError as e:
            print(f"Error downloading file from S3: {e}")
            return None
