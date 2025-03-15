import os
import sys
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Add the directory containing scraper.py to the Python path
sys.path.append('/home/kburla/src/projects/github_trending_pipeline')

from scraper import scrape_github_data, create_tables
from insert_data import insert_data

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2025, 3, 15, 14, 0, 0),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

# Define the DAG
dag = DAG(
    'github_trending_pipeline',
    default_args=default_args,
    description='A simple GitHub trending scraper pipeline',
    schedule_interval=timedelta(hours=1)
)

# Define a task to scrape the data
def scrape_and_load_data():
    create_tables()
    
    daily_data = scrape_github_data("https://github.com/trending?since=daily")
    insert_data(daily_data, 'daily')
    
    weekly_data = scrape_github_data("https://github.com/trending?since=weekly")
    insert_data(weekly_data, 'weekly')
    
    monthly_data = scrape_github_data("https://github.com/trending?since=monthly")
    insert_data(monthly_data, 'monthly')
    
# Define the task in Airflow
scrape_task = PythonOperator(
    task_id='scrape_and_load_data',
    python_callable=scrape_and_load_data,
    dag=dag,
)

scrape_task