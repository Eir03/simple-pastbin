from io import BytesIO
from minio import Minio
from config import BLOB_ACCESS_KEY, BLOB_SECRET_KEY, BLOB_SECURE, URL_BLOB

# Инициализация клиента MinIO
minio_client = Minio(
    "192.168.195.107:9000",
    access_key=BLOB_ACCESS_KEY,
    secret_key=BLOB_SECRET_KEY,
    secure=False
)

def create_bucket_if_not_exists(bucket_name: str):
    if not minio_client.bucket_exists(bucket_name):
        minio_client.make_bucket(bucket_name)

def upload_text_to_minio(bucket_name: str, object_name: str, content: str):
    try:
        # Создаем ведро, если оно не существует
        create_bucket_if_not_exists(bucket_name)
        
        # Преобразуем текст в байты
        content_bytes = content.encode('utf-8')
        content_stream = BytesIO(content_bytes)
        
        # Загрузка текста в MinIO
        minio_client.put_object(
            bucket_name=bucket_name,
            object_name=object_name,
            data=content_stream,
            length=len(content_bytes),
            content_type='text/plain'
        )
        
        # Возвращаем URL загруженного объекта
        return f"http://{URL_BLOB}/{bucket_name}/{object_name}"
    except Exception as ex:
        print(f"Ошибка при загрузке в MinIO: {ex}")
        return None