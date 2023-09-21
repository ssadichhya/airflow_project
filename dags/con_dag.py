import findspark
findspark.init()
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from pyspark.sql import SparkSession

dag = DAG(
    dag_id="read_write",
    start_date=datetime(2023, 1, 1),
    schedule_interval=" 0 0 * * *",
    catchup=False,

)

read_postgres_task = PostgresOperator(
    task_id='read_from_source_postgres',
    sql='SELECT * FROM trains',
    postgres_conn_id='postgres_conn',  
    dag=dag,
)


read_postgres_task 



