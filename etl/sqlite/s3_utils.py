import boto3

def download_json_from_s3(bucket_name, object_key, download_path, aws_access_key, aws_secret_key):
 
    s3 = boto3.client(
        's3',
        aws_access_key_id=aws_access_key,
        aws_secret_access_key=aws_secret_key
    )
    s3.download_file(bucket_name, object_key, download_path)
    print(f"File downloaded from S3: {download_path}")