import boto3
from dotenv import load_dotenv
import os

# lOAD .env file
load_dotenv()

# read environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION_NAME = os.getenv('AWS_REGION_NAME')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')

def list_s3_objects():
    
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION_NAME
    )

    # List objects in the specified S3 bucket
    response = s3_client.list_objects_v2(Bucket=S3_BUCKET_NAME)

    if 'Contents' in response:
        print(f"Bucket objects '{S3_BUCKET_NAME}':\n")
        for obj in response['Contents']:
            print(obj['Key'])
    else:
        print(f"No objects in the bucket '{S3_BUCKET_NAME}'.")

if __name__ == "__main__":
    list_s3_objects()
