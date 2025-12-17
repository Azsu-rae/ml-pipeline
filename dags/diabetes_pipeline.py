"""
Diabetes ML Pipeline DAG
Orchestrates: Extract -> Clean -> Store -> Train ML Model
"""
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
sys.path.insert(0, '/opt/airflow/scripts')

# Import our scripts
from extract import extract_data
from clean import clean_data
from store import store_data
from train_model import train_model

# Default arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# Create DAG
dag = DAG(
    'diabetes_ml_pipeline',
    default_args=default_args,
    description='ETL + ML Pipeline for Diabetes Prediction',
    schedule_interval=None,  # Manual trigger
    catchup=False,
    tags=['ml', 'etl', 'diabetes'],
)

# Task 1: Extract data from MinIO
task_extract = PythonOperator(
    task_id='extract_from_minio',
    python_callable=extract_data,
    dag=dag,
)

# Task 2: Clean and preprocess data
task_clean = PythonOperator(
    task_id='clean_and_preprocess',
    python_callable=clean_data,
    dag=dag,
)

# Task 3: Store cleaned data in PostgreSQL
task_store = PythonOperator(
    task_id='store_to_postgres',
    python_callable=store_data,
    dag=dag,
)

# Task 4: Train ML model
task_train = PythonOperator(
    task_id='train_ml_model',
    python_callable=train_model,
    dag=dag,
)

# Define task dependencies (pipeline flow)
task_extract >> task_clean >> task_store >> task_train
