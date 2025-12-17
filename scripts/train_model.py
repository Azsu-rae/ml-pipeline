"""
Task 4: ML Model - Train, evaluate, and save model
"""
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, f1_score, classification_report, confusion_matrix
import pickle
import json
import boto3
from botocore.client import Config
import os

def train_model(input_path='/tmp/diabetes_clean.csv'):
    """Train ML model on cleaned diabetes dataset"""
    
    print(f"🔹 [T4] Starting ML model training...")
    
    # Load cleaned data
    df = pd.read_csv(input_path)
    print(f"📊 Dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 1. Prepare features and target
    print("\n1️⃣ Preparing features and target...")
    
    # Select features (use encoded versions)
    feature_cols = [
        'age', 'bmi', 'hbA1c_level', 'blood_glucose_level',
        'hypertension', 'heart_disease',
        'gender_encoded', 'smoking_encoded',
        'race:AfricanAmerican', 'race:Asian', 'race:Caucasian', 
        'race:Hispanic', 'race:Other'
    ]
    
    # Filter only existing columns
    feature_cols = [col for col in feature_cols if col in df.columns]
    
    X = df[feature_cols]
    y = df['diabetes']
    
    print(f"   Features: {len(feature_cols)}")
    print(f"   Target distribution: {y.value_counts().to_dict()}")
    
    # 2. Train/Test split
    print("\n2️⃣ Splitting data (80/20)...")
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42, stratify=y
    )
    print(f"   Train: {X_train.shape[0]} samples")
    print(f"   Test: {X_test.shape[0]} samples")
    
    # 3. Train models
    print("\n3️⃣ Training models...")
    
    models = {
        'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42),
        'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, max_depth=10)
    }
    
    results = {}
    best_model = None
    best_score = 0
    
    for name, model in models.items():
        print(f"\n   Training {name}...")
        model.fit(X_train, y_train)
        
        # Predictions
        y_pred = model.predict(X_test)
        
        # Metrics
        accuracy = accuracy_score(y_test, y_pred)
        f1 = f1_score(y_test, y_pred, average='weighted')
        
        print(f"   ✅ {name}:")
        print(f"      Accuracy: {accuracy:.4f}")
        print(f"      F1-Score: {f1:.4f}")
        
        results[name] = {
            'accuracy': float(accuracy),
            'f1_score': float(f1),
            'classification_report': classification_report(y_test, y_pred, output_dict=True),
            'confusion_matrix': confusion_matrix(y_test, y_pred).tolist()
        }
        
        # Track best model
        if f1 > best_score:
            best_score = f1
            best_model = (name, model)
    
    # 4. Save best model
    print(f"\n4️⃣ Saving best model: {best_model[0]}...")
    
    model_path = '/tmp/best_model.pkl'
    with open(model_path, 'wb') as f:
        pickle.dump(best_model[1], f)
    print(f"   ✅ Model saved: {model_path}")
    
    # 5. Save metrics
    metrics_path = '/tmp/model_metrics.json'
    with open(metrics_path, 'w') as f:
        json.dump({
            'best_model': best_model[0],
            'results': results,
            'feature_importance': dict(zip(feature_cols, 
                best_model[1].feature_importances_.tolist())) if hasattr(best_model[1], 'feature_importances_') else None
        }, f, indent=2)
    print(f"   ✅ Metrics saved: {metrics_path}")
    
    # 6. Upload to MinIO (optional)
    print("\n5️⃣ Uploading artifacts to MinIO...")
    try:
        upload_to_minio(model_path, 'best_model.pkl')
        upload_to_minio(metrics_path, 'model_metrics.json')
        print("   ✅ Artifacts uploaded to MinIO")
    except Exception as e:
        print(f"   ⚠️  MinIO upload failed (optional): {str(e)}")
    
    print(f"\n✅ Model training complete!")
    print(f"🏆 Best Model: {best_model[0]} (F1: {best_score:.4f})")
    
    return results

def upload_to_minio(file_path, object_name):
    """Upload file to MinIO"""
    MINIO_ENDPOINT = os.getenv('MINIO_ENDPOINT', 'minio:9000')
    MINIO_ACCESS_KEY = os.getenv('MINIO_ACCESS_KEY', 'minioadmin')
    MINIO_SECRET_KEY = os.getenv('MINIO_SECRET_KEY', 'minioadmin')
    BUCKET_NAME = os.getenv('BUCKET_NAME', 'diabetes-data')
    
    s3_client = boto3.client(
        's3',
        endpoint_url=f'http://{MINIO_ENDPOINT}',
        aws_access_key_id=MINIO_ACCESS_KEY,
        aws_secret_access_key=MINIO_SECRET_KEY,
        config=Config(signature_version='s3v4'),
        region_name='us-east-1'
    )
    
    s3_client.upload_file(file_path, BUCKET_NAME, object_name)

if __name__ == "__main__":
    train_model()
