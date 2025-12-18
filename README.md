# Diabetes ML Pipeline - Cloud Project

# Video Presentation

Complete ETL + ML pipeline using Docker, Airflow, MinIO, and PostgreSQL.

## 🏗️ Architecture

```
┌─────────────┐     ┌──────────────┐     ┌──────────────┐     ┌──────────────┐
│   MinIO     │────▶│   Extract    │────▶│    Clean     │────▶│    Store     │
│  (Storage)  │     │   (Task 1)   │     │   (Task 2)   │     │   (Task 3)   │
└─────────────┘     └──────────────┘     └──────────────┘     └──────────────┘
                                                                       │
                                                                       ▼
                    ┌──────────────┐                          ┌──────────────┐
                    │  ML Model    │◀─────────────────────────│  PostgreSQL  │
                    │   (Task 4)   │                          │  (Database)  │
                    └──────────────┘                          └──────────────┘
```

## 📦 Components

- **MinIO**: Object storage for raw data and ML artifacts
- **PostgreSQL**: Relational database for cleaned data
- **Apache Airflow**: Workflow orchestration
- **Python Scripts**: ETL + ML logic

## 🚀 Quick Start

### 1. Start all services
```bash
docker-compose up -d
```

### 2. Wait for services to be ready (~2 minutes)
```bash
docker-compose ps
```

### 3. Setup MinIO bucket and upload dataset
```bash
docker run --rm --network ml-pipeline_default \
  -v $(pwd)/diabetes_raw.csv:/data/diabetes_raw.csv \
  -v $(pwd)/config/setup_minio.sh:/setup.sh \
  --entrypoint /bin/bash \
  minio/mc /setup.sh
```

### 4. Create PostgreSQL database
```bash
docker exec -it postgres bash -c "PGPASSWORD=airflow psql -U airflow -c 'CREATE DATABASE diabetes_db;'"
```

### 5. Access Airflow UI
- URL: http://localhost:8080
- Username: `admin`
- Password: `admin`

### 6. Trigger the DAG
1. Go to Airflow UI
2. Find `diabetes_ml_pipeline` DAG
3. Click the play button to trigger

## 📊 Access Services

| Service | URL | Credentials |
|---------|-----|-------------|
| Airflow | http://localhost:8080 | admin / admin |
| MinIO Console | http://localhost:9001 | minioadmin / minioadmin |
| PostgreSQL | localhost:5432 | airflow / airflow |

## 🔍 Pipeline Tasks

1. **Extract** (`extract.py`): Download CSV from MinIO
2. **Clean** (`clean.py`): Handle missing values, normalize, encode
3. **Store** (`store.py`): Load to PostgreSQL with proper schema
4. **Train** (`train_model.py`): Train ML models, save metrics

## 📈 SQL Analysis

Run analytical queries:
```bash
docker exec -it airflow-webserver python /opt/airflow/scripts/run_sql_analysis.py
```

Or connect to PostgreSQL directly:
```bash
docker exec -it postgres psql -U airflow -d diabetes_db
```

Then run queries from `sql/analysis_queries.sql`

## 🛑 Stop Services

```bash
docker-compose down
```

To remove volumes (clean slate):
```bash
docker-compose down -v
```

## 📁 Project Structure

```
ml-pipeline/
├── docker-compose.yml       # Infrastructure definition
├── requirements.txt         # Python dependencies
├── diabetes_raw.csv         # Dataset (100k rows)
├── dags/
│   └── diabetes_pipeline.py # Airflow DAG
├── scripts/
│   ├── extract.py          # Task 1
│   ├── clean.py            # Task 2
│   ├── store.py            # Task 3
│   ├── train_model.py      # Task 4
│   └── run_sql_analysis.py # SQL runner
├── sql/
│   └── analysis_queries.sql # 5 analytical queries
└── config/
    ├── setup_minio.sh      # MinIO initialization
    └── setup_postgres.sh   # PostgreSQL setup
```

## 🐛 Troubleshooting

**Airflow not starting?**
```bash
docker-compose logs airflow-webserver
```

**MinIO connection issues?**
```bash
docker exec -it minio mc admin info local
```

**PostgreSQL connection issues?**
```bash
docker exec -it postgres pg_isready -U airflow
```

## 📝 Notes

- First startup takes ~2-3 minutes for Airflow initialization
- Dataset: 100k rows, 16 features
- Models: Logistic Regression + Random Forest
- Best model and metrics saved to MinIO
