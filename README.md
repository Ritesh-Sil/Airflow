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



