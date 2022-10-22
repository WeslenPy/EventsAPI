from app import client_s3


def generate_uri(bucket_name,file):
    location = client_s3.get_bucket_location(Bucket=bucket_name)['LocationConstraint']
    base = f"https://s3-{location}.amazonaws.com/{bucket_name}/{file}"

    return base