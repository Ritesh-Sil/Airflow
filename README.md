### Install apache airflow with docker


Create a folder materials in your Documents

In this folder, download the following file: docker compose file

If you right click on the file and save it, you will end up with docker-compose.yaml.txt. Remove the .txt and keep docker-compose.yaml

Open your terminal or CMD and go into Documents/materials

Open Visual Studio Code by typing the command: code .


Right click below docker-compose.yml and create a new file .env (don't forget the dot before env)

In this file add the following lines

AIRFLOW_IMAGE_NAME=apache/airflow:2.4.2
AIRFLOW_UID=50000

and save the file

Go at the top bar of Visual Studio Code -> Terminal -> New Terminal


In your new terminal at the bottom of Visual Studio Code, type the command docker-compose up -d and hit ENTER


You will see many lines scrolled, wait until it's done. Docker is downloading Airflow to run it. It can take up to 5 mins depending on your connection. If Docker raises an error saying that it can't download the docker image, make sure you are not behind a proxy/vpn or corporate network. You may need to use your personal connection to make it work. 


Open your web browser and go to localhost:8080



Credits : Marc Lamberti



### Steps to create a DAG

1. Create a file user_processing.py
2. Import the DAG object, this how airflow knows that this is a DAG file.
```
from airflow import DAG
```
3. Intantiate the DAG object

```
with DAG(....)
```
4. Pass the unique ID of the DAG as a first parameter.This ID must be unique.

```
with DAG('user_processing')
```
5. Start date and import datetime

```
form datetime import datetime
with DAG('user_processing', start_date=datetime(2022,1,1))
```

6. Schedule interval

```
form datetime import datetime
with DAG('user_processing', start_date=datetime(2022,1,1),
            schedule_interval='@daily')
```

7. catchup parameter.

```
form datetime import datetime
with DAG('user_processing', start_date=datetime(2022,1,1),
            schedule_interval='@daily', catchup = False)

```

8. Finally add 'as dag' part and 'None'

```
form datetime import datetime
with DAG('user_processing', start_date=datetime(2022,1,1),
            schedule_interval='@daily', catchup = False) as dag:
            None

```


### Steps in summary

1. Import the DAG object
2. Instantiate a the DAG object
3. Define a unique dag id
4. Define a start date
5. Define a scheduled interval
6. Define the catchup parameter


### Operators and its types

Operators defines tasks.
A single task is to be defined by a single operator.

3 Types of operators:

1. Action operator
2. Transfer operator
3. Sensor operator.

### Providers

Whenever you need to integrate 3rd party services you need the providers. 

In such case we need to install the plug ins like:

pip install apache-airflow-providers-snowflake
pip install apache-airflow-providers-databricks
pip install apache-airflow-providers-dbt
pip install apache-airflow-providers-aws


### Create a table

In order to perform a SQL request to postgres database and create a table.

```
from airflow import DAG

from airflow.providers.postgres.operators.postgres import PostgresOperator

from date import datetime


with DAG(

    'user_processing',
    start_date = datetime(2022,1,1),
    schedule_interval='@daily',
    catchup=False
) as dag:

    create_table = PostgresOperator(

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


```

### Create a connection

Any operator in Airflow DAG interacts with external service needs a connection.

This is to be defined in Admin --> Connection in Airflow UI.

### Tesing the DAG

It is always recommended to test the task and schedule from the airflow CLI.

To do that, we need to execute the below set of commands.

```
docker-compose ps : It will show all the container

docker exec -it materials_airflow-scheduler_1 /bin/bash : Containers responsible for scheduling. From here you can access the airflow CLI


airflow -h : All the commands with airflow CLI

airflow tasks test user_processing create_table 2022-01-01

```
Press : ctrl + d to go back to the original container.

### The Sensors
Wait for something to happen or change.

2 parameters 
1. poke_interval : 60 sec by default, every 60 seconds the sensor checks if the connection is true or not.

2. timeout : by default 7 days


### Is API available

To check if the the api is available or not.

```
from airflow.providers.http.sensors.http import HttpSensor

is_api_available =HttpSensor(

    task_id = 'is_api_available',
    http_connection_id = 'user_api',
    endpoint = 'api/'
)


```


### Extract Users

```
from airflow.providers.http.sensors.http import SimpleHttpOperator
import json


extact_user = SimpleHttpOperator(

    task_id = 'extact_user',
    http_conn_ id = 'user_api',
    enpoint = 'api/',
    method = 'GET',
    response_filter = lambda response: json.loads(response.text),
    log_response = True
    )



```

### Process Users

Use PythonOperator to execute python functions.

```
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
    


process_user = PythonOperator(

    task_id = 'process_user',
    python_callable = _process_user // This is the function to defined before the DAG



)

```

### What is Hook

Hooks allows us to easily interact with the external tools or services.

### Create dependencies

Need to use '>>' operator between two tasks to set dependencies.

### DAG in action
