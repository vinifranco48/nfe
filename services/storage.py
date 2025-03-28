import os
import logging
import boto3
from config import MINIO_ENDPOINT, MINIO_ACCESS_KEY, MINIO_SECRET_KEY, BUCKET_NAME
import io
import json

def get_s3_client():
    try:
        return boto3.client(
            's3',
            endpoint_url=MINIO_ENDPOINT,
            aws_access_key_id=MINIO_ACCESS_KEY,
            aws_secret_access_key=MINIO_SECRET_KEY,
            region_name="us-east-1"
        )
    except Exception as e:
        logging.error(f"Failed to create S3 client: {e}")
        raise

s3_client = get_s3_client()

def setup_minio_bucket(bucket_name: str):
    try:
        s3_client.head_bucket(Bucket=bucket_name)
        logging.info(f"Bucket '{bucket_name}' já existe.")
    except Exception:
        s3_client.create_bucket(Bucket=bucket_name)
        logging.info(f"Bucket '{bucket_name}' criado.")
def upload_json_to_minio(json_data: dict, bucket: str, object_name: str):
    try:
        # Converte o dicionário em uma string JSON e depois em bytes
        json_bytes = json.dumps(json_data).encode('utf-8')
        # Cria um objeto BytesIO para upload
        bytes_obj = io.BytesIO(json_bytes)
        s3_client.upload_fileobj(bytes_obj, bucket, object_name)
        logging.info(f"Arquivo JSON '{object_name}' enviado com sucesso para o bucket '{bucket}'.")
    except Exception as e:
        logging.error(f"Erro ao enviar arquivo JSON para o MinIO: {e}")
        raise
setup_minio_bucket(BUCKET_NAME)
