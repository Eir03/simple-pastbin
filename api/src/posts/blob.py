from io import BytesIO
from config import BLOB_ACCESS_KEY, BLOB_SECRET_KEY, URL_BLOB, USE_BLOB
from botocore.exceptions import NoCredentialsError, ClientError
import boto3

class Blob:
    """Класс для работы с S3 совместимыми хранилищами"""
    def __init__(self):
        self.use_blob = USE_BLOB
        if self.use_blob:
            self.session = boto3.session.Session()
            self.s3 = boto3.client(
                's3',
                endpoint_url=URL_BLOB,
                aws_access_key_id=BLOB_ACCESS_KEY,
                aws_secret_access_key=BLOB_SECRET_KEY
            )

    def _check_blob_enabled(self):
        """Приватный метод, чтобы избежать лишнего кода в методах"""

        if not self.use_blob:
            print("[SKIP] Хранилище BLOB не используется.")
            return False
        return True
    
    def create_bucket_if_not_exists(self, bucket_name: str):
        if not self._check_blob_enabled():
            return
        try:
            response = self.s3.list_buckets()
            if not any(bucket['Name'] == bucket_name for bucket in response['Buckets']):
                self.s3.create_bucket(Bucket=bucket_name)
                print(f"Бакет {bucket_name} создан.")
        except ClientError as e:
            print(f"Ошибка при создании бакета: {e}")

    def upload_text_to_s3(self, bucket_name: str, object_name: str, content: str):
        if not self._check_blob_enabled():
            return
        try:
            self.create_bucket_if_not_exists(bucket_name)
            
            content_bytes = content.encode('utf-8')
            
            self.s3.put_object(
                Bucket=bucket_name,
                Key=object_name,
                Body=content_bytes,
                ContentType='text/plain'
            )
            
            return f"{URL_BLOB}/{bucket_name}/{object_name}"
        
        except (NoCredentialsError, ClientError) as e:
            print(f"Ошибка при загрузке в S3: {e}")
            return None
        
    def delete_object_from_s3(self, bucket_name: str, object_name: str):
        if not self._check_blob_enabled():
            return
        try:
            self.s3.delete_object(Bucket=bucket_name, Key=object_name)
            return True
        except (NoCredentialsError, ClientError) as e:
            print(f"Ошибка при удалении из S3: {e}")
            return False