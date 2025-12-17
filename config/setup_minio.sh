#!/bin/bash
# Setup script to initialize MinIO bucket and upload dataset

echo "🔹 Waiting for MinIO to be ready..."
sleep 10

echo "🔹 Installing MinIO client..."
wget -q https://dl.min.io/client/mc/release/linux-amd64/mc -O /usr/local/bin/mc
chmod +x /usr/local/bin/mc

echo "🔹 Configuring MinIO client..."
mc alias set myminio http://minio:9000 minioadmin minioadmin

echo "🔹 Creating bucket: diabetes-data..."
mc mb myminio/diabetes-data --ignore-existing

echo "🔹 Uploading diabetes dataset..."
mc cp /data/diabetes_raw.csv myminio/diabetes-data/diabetes_raw.csv

echo "✅ MinIO setup complete!"
mc ls myminio/diabetes-data
