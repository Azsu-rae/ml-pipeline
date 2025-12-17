"""
Task 3: Store - Load cleaned data into PostgreSQL
"""
import pandas as pd
import psycopg2
from psycopg2 import sql
from sqlalchemy import create_engine
import os

def store_data(input_path='/tmp/diabetes_clean.csv'):
    """Load cleaned dataset into PostgreSQL"""
    
    print(f"🔹 [T3] Starting data storage to PostgreSQL...")
    
    # PostgreSQL connection settings
    PG_HOST = os.getenv('POSTGRES_HOST', 'postgres')
    PG_PORT = os.getenv('POSTGRES_PORT', '5432')
    PG_DB = os.getenv('POSTGRES_DB', 'diabetes_db')
    PG_USER = os.getenv('POSTGRES_USER', 'airflow')
    PG_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'airflow')
    
    # Load cleaned data
    df = pd.read_csv(input_path)
    print(f"📊 Loading {df.shape[0]} rows into PostgreSQL...")
    
    # Create SQLAlchemy engine
    connection_string = f'postgresql://{PG_USER}:{PG_PASSWORD}@{PG_HOST}:{PG_PORT}/{PG_DB}'
    engine = create_engine(connection_string)
    
    try:
        # Create table with proper types
        print("\n1️⃣ Creating table schema...")
        
        conn = psycopg2.connect(
            host=PG_HOST,
            port=PG_PORT,
            database=PG_DB,
            user=PG_USER,
            password=PG_PASSWORD
        )
        cursor = conn.cursor()
        
        # Drop table if exists
        cursor.execute("DROP TABLE IF EXISTS diabetes_clean CASCADE;")
        
        # Create table with normalized types
        create_table_query = """
        CREATE TABLE diabetes_clean (
            id SERIAL PRIMARY KEY,
            year INTEGER,
            gender VARCHAR(10),
            age FLOAT,
            location VARCHAR(50),
            race_african_american INTEGER,
            race_asian INTEGER,
            race_caucasian INTEGER,
            race_hispanic INTEGER,
            race_other INTEGER,
            hypertension INTEGER,
            heart_disease INTEGER,
            smoking_history VARCHAR(20),
            bmi FLOAT,
            hba1c_level FLOAT,
            blood_glucose_level FLOAT,
            diabetes INTEGER,
            gender_encoded INTEGER,
            smoking_encoded INTEGER,
            location_encoded INTEGER
        );
        """
        
        cursor.execute(create_table_query)
        conn.commit()
        print("   ✅ Table created successfully")
        
        # 2. Load data using pandas to_sql
        print("\n2️⃣ Inserting data...")
        
        # Rename columns to match SQL naming convention
        df_to_load = df.copy()
        df_to_load.columns = [col.replace(':', '_').lower() for col in df_to_load.columns]
        
        # Insert data
        df_to_load.to_sql(
            'diabetes_clean',
            engine,
            if_exists='append',
            index=False,
            method='multi',
            chunksize=1000
        )
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM diabetes_clean;")
        count = cursor.fetchone()[0]
        print(f"   ✅ Inserted {count} rows")
        
        # Create indexes for better query performance
        print("\n3️⃣ Creating indexes...")
        cursor.execute("CREATE INDEX idx_age ON diabetes_clean(age);")
        cursor.execute("CREATE INDEX idx_diabetes ON diabetes_clean(diabetes);")
        cursor.execute("CREATE INDEX idx_bmi ON diabetes_clean(bmi);")
        print("   ✅ Indexes created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\n✅ Data successfully stored in PostgreSQL!")
        print(f"📊 Table: diabetes_clean ({count} rows)")
        
    except Exception as e:
        print(f"❌ Error storing data: {str(e)}")
        raise
    finally:
        engine.dispose()

if __name__ == "__main__":
    store_data()
