# 🚀 Quick Start Guide - 3 Hour Deadline Edition

## ⚡ Fast Track (5 Steps)

### Step 1: Start Everything (2-3 minutes)
```bash
make start
```
Wait for services to initialize. Check status:
```bash
docker-compose ps
```
All services should show "Up" or "healthy".

### Step 2: Setup Infrastructure (1 minute)
```bash
make setup
```
This creates the database and uploads your dataset to MinIO.

### Step 3: Access Airflow (30 seconds)
Open browser: http://localhost:8080
- Username: `admin`
- Password: `admin`

### Step 4: Run the Pipeline (5 minutes)
In Airflow UI:
1. Find DAG: `diabetes_ml_pipeline`
2. Toggle it ON (switch on the left)
3. Click the ▶️ play button (top right)
4. Watch the tasks turn green!

### Step 5: Run SQL Analysis (30 seconds)
```bash
make sql-analysis
```

## ✅ What You'll See

**Pipeline Tasks (in order):**
1. 🔹 **extract_from_minio** - Downloads CSV (10 sec)
2. 🔹 **clean_and_preprocess** - Cleans data (30 sec)
3. 🔹 **store_to_postgres** - Loads to DB (1 min)
4. 🔹 **train_ml_model** - Trains models (2-3 min)

**Results:**
- ✅ Cleaned data in PostgreSQL
- ✅ ML models trained (Logistic Regression + Random Forest)
- ✅ Metrics saved to MinIO
- ✅ SQL analysis complete

## 🐛 Quick Fixes

**Services not starting?**
```bash
docker-compose down -v
make start
```

**Airflow stuck?**
```bash
docker-compose restart airflow-scheduler
```

**Need to see logs?**
```bash
docker-compose logs -f airflow-scheduler
```

## 📊 Verify Everything Works

1. **MinIO**: http://localhost:9001 (minioadmin/minioadmin)
   - Check bucket `diabetes-data` has files

2. **PostgreSQL**:
   ```bash
   docker exec -it postgres psql -U airflow -d diabetes_db -c "SELECT COUNT(*) FROM diabetes_clean;"
   ```
   Should show 100,000 rows

3. **Airflow**: http://localhost:8080
   - All 4 tasks should be green

## ⏱️ Total Time: ~10 minutes

Good luck! 🍀
