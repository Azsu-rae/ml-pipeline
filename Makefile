.PHONY: help start stop restart logs setup-minio setup-postgres run-pipeline clean

help:
	@echo "🚀 Diabetes ML Pipeline - Available Commands"
	@echo ""
	@echo "  make start          - Start all Docker services"
	@echo "  make stop           - Stop all services"
	@echo "  make restart        - Restart all services"
	@echo "  make logs           - View logs from all services"
	@echo "  make setup-minio    - Initialize MinIO and upload dataset"
	@echo "  make setup-postgres - Create PostgreSQL database"
	@echo "  make setup          - Run both setup commands"
	@echo "  make run-pipeline   - Trigger Airflow DAG manually"
	@echo "  make sql-analysis   - Run SQL analytical queries"
	@echo "  make clean          - Stop and remove all containers/volumes"
	@echo ""

start:
	@echo "🔹 Starting all services..."
	docker-compose up -d
	@echo "✅ Services started! Waiting for initialization..."
	@sleep 10
	@echo "📊 Service status:"
	docker-compose ps

stop:
	@echo "🔹 Stopping all services..."
	docker-compose down

restart:
	@echo "🔹 Restarting services..."
	docker-compose restart

logs:
	docker-compose logs -f

setup-minio:
	@echo "🔹 Setting up MinIO bucket and uploading dataset..."
	docker run --rm --network ml-pipeline_default \
		-v $(PWD)/diabetes_raw.csv:/data/diabetes_raw.csv \
		-v $(PWD)/config/setup_minio.sh:/setup.sh \
		--entrypoint /bin/bash \
		minio/mc /setup.sh

setup-postgres:
	@echo "🔹 Creating PostgreSQL database..."
	docker exec -it postgres bash -c "PGPASSWORD=airflow psql -U airflow -c 'CREATE DATABASE diabetes_db;'" || true
	@echo "✅ Database created!"

setup: setup-postgres setup-minio
	@echo "✅ Setup complete! Access Airflow at http://localhost:8080 (admin/admin)"

run-pipeline:
	@echo "🔹 Triggering Airflow DAG..."
	docker exec -it airflow-webserver airflow dags trigger diabetes_ml_pipeline
	@echo "✅ Pipeline triggered! Check progress at http://localhost:8080"

sql-analysis:
	@echo "🔹 Running SQL analysis..."
	docker exec -it airflow-webserver python /opt/airflow/scripts/run_sql_analysis.py

clean:
	@echo "🔹 Cleaning up all containers and volumes..."
	docker-compose down -v
	@echo "✅ Cleanup complete!"
