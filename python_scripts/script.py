from pyspark.sql import SparkSession
from pyspark.sql.functions import col,count
import os



spark = SparkSession.builder \
        .appName("PostgresToDataFrame") \
        .config("spark.jars", "/usr/lib/jvm/java-11-openjdk-amd64/lib/postgresql-42.6.0.jar") \
        .getOrCreate()

user_df = spark.read.format("jdbc").option("url", "jdbc:postgresql://localhost:5432/airflow_input") \
        .option("driver", "org.postgresql.Driver").option("dbtable", "user_input_table") \
        .option("user", "postgres").option("password", "postgres").load()
# user_df.show()

gender_count = user_df.groupBy("gender").count()
gender_count.show()

# email_domains = user_df.selectExpr("DISTINCT SUBSTRING_INDEX(email, '@', -1) AS email_domain")
# email_domains.show()

gender_counts = user_df.groupBy("gender").agg(count("*").alias("gender_count"))
total_count = user_df.count()
gender_percentage = gender_counts.withColumn(
    "percentage",
    (col("gender_count") * 100.0 / total_count)
)
gender_percentage.show()

# Calculate the count of each status
status_counts = user_df.groupBy("status").count()
status_counts.show()


gender_percentage.write.parquet("/home/ubuntu/airflow/airflow_output/gender_percentage.parquet", mode="overwrite")
gender_count.write.parquet("/home/ubuntu/airflow/airflow_output/gender_count.parquet", mode="overwrite")
status_counts.write.parquet("/home/ubuntu/airflow/airflow_output/status_counts.parquet", mode="overwrite")

jdbc_url = "jdbc:postgresql://localhost:5432/airflow_output"
properties = {
    "user": "postgres",
    "password": "postgres",
    "driver": "org.postgresql.Driver"
}


gender_percentage.write.jdbc(url=jdbc_url, table='gender_percentage_table', mode="overwrite", properties=properties)
gender_count.write.jdbc(url=jdbc_url, table='gender_count', mode="overwrite", properties=properties)
status_counts.write.jdbc(url=jdbc_url, table='status_counts', mode="overwrite", properties=properties)


spark.stop()
