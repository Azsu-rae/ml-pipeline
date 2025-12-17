"""
Task 2: Clean - Data cleaning and preprocessing
Handles missing values, normalization, encoding
"""
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
import pickle

def clean_data(input_path='/tmp/diabetes_raw.csv', output_path='/tmp/diabetes_clean.csv'):
    """Clean and preprocess diabetes dataset"""
    
    print(f"🔹 [T2] Starting data cleaning...")
    
    # Load data
    df = pd.read_csv(input_path)
    print(f"📊 Original dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    
    # 1. Handle missing values
    print("\n1️⃣ Handling missing values...")
    initial_nulls = df.isnull().sum().sum()
    print(f"   Missing values found: {initial_nulls}")
    
    # Replace 'No Info' in smoking_history with mode
    if 'smoking_history' in df.columns:
        mode_smoking = df[df['smoking_history'] != 'No Info']['smoking_history'].mode()[0]
        df['smoking_history'] = df['smoking_history'].replace('No Info', mode_smoking)
    
    # Fill numeric missing values with median
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    for col in numeric_cols:
        if df[col].isnull().sum() > 0:
            df[col].fillna(df[col].median(), inplace=True)
    
    print(f"   ✅ Missing values after cleaning: {df.isnull().sum().sum()}")
    
    # 2. Encoding categorical variables
    print("\n2️⃣ Encoding categorical variables...")
    
    # Gender encoding
    if 'gender' in df.columns:
        df['gender_encoded'] = df['gender'].map({'Male': 1, 'Female': 0})
        print(f"   ✅ Encoded gender")
    
    # Smoking history encoding (ordinal)
    if 'smoking_history' in df.columns:
        smoking_map = {
            'never': 0,
            'No Info': 1,
            'former': 2,
            'not current': 2,
            'current': 3,
            'ever': 2
        }
        df['smoking_encoded'] = df['smoking_history'].map(smoking_map)
        print(f"   ✅ Encoded smoking_history")
    
    # Location encoding (if needed, use one-hot or label encoding)
    if 'location' in df.columns:
        df['location_encoded'] = pd.factorize(df['location'])[0]
        print(f"   ✅ Encoded location")
    
    # 3. Normalization/Scaling
    print("\n3️⃣ Normalizing numerical features...")
    
    # Features to scale
    scale_features = ['age', 'bmi', 'hbA1c_level', 'blood_glucose_level']
    scale_features = [f for f in scale_features if f in df.columns]
    
    scaler = StandardScaler()
    df[scale_features] = scaler.fit_transform(df[scale_features])
    
    # Save scaler for later use
    with open('/tmp/scaler.pkl', 'wb') as f:
        pickle.dump(scaler, f)
    
    print(f"   ✅ Scaled features: {', '.join(scale_features)}")
    
    # 4. Feature engineering (optional but good practice)
    print("\n4️⃣ Feature engineering...")
    
    # BMI categories
    if 'bmi' in df.columns:
        # Note: bmi is now scaled, so we'll create this before scaling in production
        # For now, we'll skip or use original values
        pass
    
    # Age groups
    if 'age' in df.columns:
        # Create age groups (before scaling ideally)
        pass
    
    # 5. Save cleaned dataset
    print("\n5️⃣ Saving cleaned dataset...")
    df.to_csv(output_path, index=False)
    
    print(f"✅ Cleaned dataset saved: {output_path}")
    print(f"📊 Final dataset: {df.shape[0]} rows, {df.shape[1]} columns")
    print(f"\n📋 Columns: {list(df.columns)}")
    
    return output_path

if __name__ == "__main__":
    clean_data()
