from app import client_s3

def generate_uri(bucket_name,file):
    base = f"https://s3.amazonaws.com/{bucket_name}/{file}"
    return base