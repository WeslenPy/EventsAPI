from .generate_url import generate_uri
from app.server.instance import app  
import boto3

s3,bucket_name = app.s3,app.bucket_name

def upload_file(file:bytes,file_name:str)->str:
    bucket = s3.Bucket(bucket_name)

    bucket.upload_fileobj(file,file_name)
    return generate_uri(bucket_name,file_name)
