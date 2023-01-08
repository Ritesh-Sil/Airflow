from airflow import DAG
from date import datetime

with DAG('user_processing', start_date=(2023,1,1), schedule='@daily', catchup = False) as dag:
    None