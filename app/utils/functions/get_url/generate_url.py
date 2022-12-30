
def generate_uri(bucket_name,file):
    base = f"https://{bucket_name}.s3.sa-east-1.amazonaws.com/{file}"
    return base