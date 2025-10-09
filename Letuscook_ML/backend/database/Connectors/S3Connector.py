import os
import traceback
import boto3

from dotenv import load_dotenv
from common.CommonFunc import getProjectRoot

class S3Connector:
    def __init__(self):
        rootpath = getProjectRoot()
        load_dotenv(dotenv_path=rootpath/'.env')
        # AWS config
        self.AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
        self.AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
        self.AWS_REGION = os.getenv("AWS_REGION")
        self.AWS_BUCKET_NAME = os.getenv("AWS_BUCKET_NAME")
        # connect
        self.connects3()
    def connects3(self):
        try:
            self.s3 = boto3.client(
                "s3",
                aws_access_key_id=self.AWS_ACCESS_KEY_ID,
                aws_secret_access_key=self.AWS_SECRET_ACCESS_KEY,
                region_name=self.AWS_REGION,
            )
        except :
            traceback.print_exc()
            return None

    def upload_avatar(self, file_path, user_id):
        """Upload file lên S3"""
        try:
            file_name = os.path.basename(file_path)
            s3_key = f"avatars/{user_id}_{file_name}"

            self.s3.upload_file(
                Filename=file_path,
                Bucket=self.AWS_BUCKET_NAME,
                Key=s3_key,
                ExtraArgs={'ContentType': 'image/jpeg'}
            )
            photo_url = f"https://{self.AWS_BUCKET_NAME}.s3.{self.AWS_REGION}.amazonaws.com/{s3_key}"
            return photo_url
        except :
            traceback.print_exc()
            return None

