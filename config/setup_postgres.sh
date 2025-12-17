#!/bin/bash
# Initialize PostgreSQL database for diabetes data

echo "🔹 Waiting for PostgreSQL to be ready..."
sleep 5

echo "🔹 Creating diabetes_db database..."
PGPASSWORD=airflow psql -h postgres -U airflow -d airflow -c "CREATE DATABASE diabetes_db;" 2>/dev/null || echo "Database already exists"

echo "✅ PostgreSQL setup complete!"
PGPASSWORD=airflow psql -h postgres -U airflow -d airflow -c "\l" | grep diabetes_db
