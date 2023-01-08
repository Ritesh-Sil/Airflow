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






