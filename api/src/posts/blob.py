from io import BytesIO
from minio import Minio
from config import BLOB_ACCESS_KEY, BLOB_SECRET_KEY, BLOB_SECURE, URL_BLOB, BUCKET
from botocore.exceptions import NoCredentialsError, ClientError
import boto3

session = boto3.session.Session()
s3 = boto3.client(
    's3',
    endpoint_url=URL_BLOB,
    aws_access_key_id=BLOB_ACCESS_KEY,
    aws_secret_access_key=BLOB_SECRET_KEY
)

def create_bucket_if_not_exists(bucket_name: str):
    try:
        response = s3.list_buckets()
        if not any(bucket['Name'] == bucket_name for bucket in response['Buckets']):
            s3.create_bucket(Bucket=bucket_name)
            print(f"Бакет {bucket_name} создан.")
    except ClientError as e:
        print(f"Ошибка при создании бакета: {e}")

def upload_text_to_s3(bucket_name: str, object_name: str, content: str):
    try:
        create_bucket_if_not_exists(bucket_name)
        
        content_bytes = content.encode('utf-8')
        
        s3.put_object(
            Bucket=bucket_name,
            Key=object_name,
            Body=content_bytes,
            ContentType='text/plain'
        )
        
        return f"{URL_BLOB}/{bucket_name}/{object_name}"
    
    except (NoCredentialsError, ClientError) as e:
        print(f"Ошибка при загрузке в S3: {e}")
        return None