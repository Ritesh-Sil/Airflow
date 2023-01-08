from airflow import DAG
from datetime import datetime
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.providers.http.sensors.http import HttpSensor
from airflow.providers.http.operators.http import SimpleHttpOperator
import json

from airflow.operators.python import PythonOperator
from pandas import json_normalize

def _process_users(ti):
    user = ti.xcom_pull(task_ids="extract_user")
    user = user['results'][0]
    processed_user = json_normalize({
        'firstname':user['name']['first'],
        'lastname':user['name']['last'],
        'country':user['location']['country'],
        'username':user['login']['username'],
        'password':user['login']['password'],
        'email':user['email']  })
    processed_user.to_csv('/tmp/processed_user.csv', index=None, header=False)

with DAG('user_processing', start_date=datetime(2022, 1, 1), 
        schedule_interval='@daily', catchup=False) as dag:

    create_table=PostgresOperator(
        task_id  = 'create_table',
        postgres_conn_id = 'postgres',
        sql=
        '''
            CREATE TABLE IF NOT EXISTS USERS
            (
                FIRST_NAME TEXT NOT null,
                LAST_NAME TEXT NOT null,
                COUNTRY TEXT NOT null,
                USERNAME TEXT NOT null,
                PASSWORD TEXT NOT null,
                EMAIL TEXT NOT null
            );
        
        '''

    
    )

    is_api_available = HttpSensor(
        task_id = 'is_api_available',
        http_conn_id = 'user_api',
        endpoint = 'api/'
    )

    extact_user = SimpleHttpOperator(
        task_id = 'extact_user',
        http_conn_id = 'user_api',
        endpoint = 'api/',
        method = 'GET',
        response_filter = lambda response: json.loads(response.text),
        log_response = True
    )

    process_user = PythonOperator(

    task_id = 'process_user',
    python_callable = _process_users
    )

create_table >> is_api_available >> extact_user >> process_user
