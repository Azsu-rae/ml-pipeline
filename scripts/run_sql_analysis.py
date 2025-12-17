"""
SQL Analysis Runner - Execute analytical queries on PostgreSQL
"""
import psycopg2
import pandas as pd
import os

def run_sql_analysis():
    """Execute all 5 analytical SQL queries"""
    
    print(f"🔹 Running SQL Analysis...")
    
    # PostgreSQL connection
    PG_HOST = os.getenv('POSTGRES_HOST', 'postgres')
    PG_PORT = os.getenv('POSTGRES_PORT', '5432')
    PG_DB = os.getenv('POSTGRES_DB', 'diabetes_db')
    PG_USER = os.getenv('POSTGRES_USER', 'airflow')
    PG_PASSWORD = os.getenv('POSTGRES_PASSWORD', 'airflow')
    
    conn = psycopg2.connect(
        host=PG_HOST,
        port=PG_PORT,
        database=PG_DB,
        user=PG_USER,
        password=PG_PASSWORD
    )
    
    # Read SQL file
    with open('/opt/airflow/sql/analysis_queries.sql', 'r') as f:
        sql_content = f.read()
    
    # Split queries (separated by double newlines or comments)
    queries = [q.strip() for q in sql_content.split(';') if q.strip() and not q.strip().startswith('--')]
    
    print(f"\n📊 Executing {len(queries)} analytical queries...\n")
    
    for i, query in enumerate(queries, 1):
        if not query or len(query) < 10:
            continue
            
        print(f"{'='*60}")
        print(f"Query {i}:")
        print(f"{'='*60}")
        
        try:
            df = pd.read_sql_query(query, conn)
            print(df.to_string(index=False))
            print(f"\n✅ Query {i} executed successfully\n")
        except Exception as e:
            print(f"❌ Error in Query {i}: {str(e)}\n")
    
    conn.close()
    print(f"✅ SQL Analysis complete!")

if __name__ == "__main__":
    run_sql_analysis()
