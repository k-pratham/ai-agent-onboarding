from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import os
import logging
from etl_pipeline.extract.excel_reader import extract_excel_data
from etl_pipeline.transform.transformer import transform_candidate_data
from etl_pipeline.load.db_loader import load_data
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Configuration
EXCEL_PATH = os.getenv("EXCEL_PATH", "/shared/excel_offer_tracker/Offer_tracker.xlsx")
# Use Oracle Dialect per specification
DB_URI = os.getenv("DB_URI", "oracle+cx_oracle://user:pass@localhost:1521/?service_name=orcl")

default_args = {
    'owner': 'hr_automation',
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

def etl_task_callable():
    logging.info("Starting ETL execution")
    
    # Extract
    raw_data = extract_excel_data(EXCEL_PATH)
    
    # Transform
    transformed_data = transform_candidate_data(raw_data)
    
    # Load
    engine = create_engine(DB_URI)
    Session = sessionmaker(bind=engine)
    with Session() as session:
        load_data(session, transformed_data)
        
    logging.info("ETL execution completed successfully")

# Defined to run daily at 10 PM IST (which is 16:30 UTC)
dag = DAG(
    'excel_onboarding_etl',
    default_args=default_args,
    description='ETL pipeline for HR Onboarding from Excel to Oracle Database',
    schedule_interval='30 16 * * *', # 4:30 PM UTC -> 10 PM IST
    catchup=False
)

etl_task = PythonOperator(
    task_id='run_excel_etl',
    python_callable=etl_task_callable,
    dag=dag,
)
