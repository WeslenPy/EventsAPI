from app import client_s3
import sys

def generate_uri(bucket_name,file):
    location = client_s3.get_bucket_location(Bucket=bucket_name)
    print(location,file=sys.stderr)
    base = f"https://s3-{location['LocationConstraint']}.amazonaws.com/{bucket_name}/{file}"

    return base