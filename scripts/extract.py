"""
Task 1: Extract - Download CSV from MinIO
"""
import boto3
import os
from botocore.client import Config

def extract_data():
    """Download diabetes dataset from MinIO"""
    
    # MinIO connection settings
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    BUCKET_NAME = os.getenv('BUCKET_NAME', 'diabetes-data')
    FILE_NAME = 'diabetes_raw.csv'
    
    print(f"🔹 [T1] Starting data extraction from MinIO...")
    
    # Initialize MinIO client
    s3_client = boto3.client(
        's3',
        endpoint_url=f'http://{MINIO_ENDPOINT}',
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
    
    # Download file
    local_path = '/tmp/diabetes_raw.csv'
    
    try:
        s3_client.download_file(BUCKET_NAME, FILE_NAME, local_path)
        print(f"✅ Successfully downloaded {FILE_NAME} from MinIO")
        print(f"📁 Saved to: {local_path}")
        
        # Verify file size
        file_size = os.path.getsize(local_path) / (1024 * 1024)  # MB
        print(f"📊 File size: {file_size:.2f} MB")
        
        return local_path
        
    except Exception as e:
        print(f"❌ Error downloading file: {str(e)}")
        raise

if __name__ == "__main__":
    extract_data()
