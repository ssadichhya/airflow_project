import json
from airflow import DAG
from airflow.providers.http.operators.http import SimpleHttpOperator
from datetime import datetime
from airflow.operators.python_operator import PythonOperator
from airflow.providers.http.sensors.http import HttpSensor
import csv
from airflow.sensors.filesystem import FileSensor  
from airflow.providers.postgres.operators.postgres import PostgresOperator
# from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator
from airflow.operators.bash_operator import BashOperator






#defining our dag
with DAG(
    dag_id="project_dag",
    start_date=datetime(2023, 9, 18),
    schedule_interval=" 0 0 * * *",
    catchup=False,
) as dag:
    #to check if the api is active or not
    task_api_active= HttpSensor(
        task_id="is_active",
        http_conn_id="project_conn",
        endpoint='users/'
    )


    task_get_users=SimpleHttpOperator(
        task_id="get_users",
        http_conn_id="project_conn",
        endpoint='users/',
        method="GET",
        response_filter=lambda response: json.loads(response.text),
        log_response=True,
    )



    def convert_json_to_csv(**kwargs):
        response_data = kwargs['ti'].xcom_pull(task_ids="get_users")  # Retrieve JSON data from the XCom
        
        if response_data:
            # Define the CSV file path
            csv_file_path = './user_data.csv' 
            
            # Write JSON data to a CSV file
            with open(csv_file_path, 'w', newline='') as csvfile:
                csv_writer = csv.writer(csvfile)
                
                header = list(response_data[0].keys())
                csv_writer.writerow(header)
                
                for item in response_data:
                    csv_writer.writerow(list(item.values()))
        else:
            print("No JSON data available in XCom to convert to CSV.")


    task_convert_to_csv = PythonOperator(
        task_id="convert_to_csv",
        python_callable=convert_json_to_csv,
        provide_context=True, 
    )

    file_sensor_task = FileSensor(
        task_id="file_sensor_task",
        filepath="/tmp/user_data.csv",  
        poke_interval=30,  # Check every 30 seconds for the file
        timeout=90,  
        mode="poke",  
    )

    load_to_postgres_task = PostgresOperator(
        task_id="load_to_postgres_task",
        postgres_conn_id="postgres_conn_1",  
        sql="""COPY user_input_table FROM '/tmp/user_data.csv' DELIMITER ',' CSV HEADER;""", 
    )


        
    # postgres_to_dataframe()
        # Filter the DataFrame to include only records with "active" status
        # filtered_df = df[df['status'] == 'active']

    # spark_submit_task = SparkSubmitOperator(
    #     task_id="spark_submit_task",
    #     conn_id="spark_default",  # Airflow connection ID for Spark
    #     application_args=["--function", "postgres_to_dataframe"],
    # )

    spark_submit_task= BashOperator(
        task_id='spark_submit_task',
        bash_command='/opt/spark/bin/spark-submit /home/ubuntu/airflow/python_scripts/script.py',
    )


    read_postgres_task = PostgresOperator(
        task_id='read_postgres_task',
        sql='SELECT * FROM gender_percentage_table',
        postgres_conn_id='postgres_conn_2',      
    )


    def display_postgres_data(**kwargs):
        ti = kwargs['ti']
        data = ti.xcom_pull(task_ids='read_postgres_task')
    
        if data:
            for row in data:
                print(row)  
        else:
            print("No data available from Postgres.")

    display_postgres_data_task = PythonOperator(
        task_id="display_postgres_data_task",
        python_callable=display_postgres_data,
        provide_context=True,
    )



     
task_api_active >> task_get_users >> task_convert_to_csv>>file_sensor_task>>load_to_postgres_task>>spark_submit_task>>read_postgres_task>>display_postgres_data_task
   
