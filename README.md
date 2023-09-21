# Airflow DAG for Project Workflow

This repository contains an Apache Airflow Directed Acyclic Graph (DAG) for a project workflow. The DAG automates various tasks related to data extraction, transformation, loading, and analysis.

## Table of Contents

- [Introduction](#introduction)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [DAG Structure](#dag-structure)
- [Contributing](#contributing)
- [License](#license)

## Introduction

This Airflow DAG is designed to automate a series of tasks for a project. It includes the following tasks:

1. **API Health Check:** This task checks whether the target API is active or not. It is essential to ensure that the API is available before proceeding with data extraction.

2. **Get Users Data:** This task makes an HTTP GET request to the API to retrieve user data. The response is filtered and processed as JSON data.

3. **Convert JSON to CSV:** The JSON data obtained from the API is converted to a CSV format. This step facilitates further data analysis and loading into a database.

4. **File Sensor:** Monitors the existence of the CSV file generated in the previous step. This task ensures that the file is ready for further processing before proceeding.

5. **Load to Postgres:** Loads the CSV data into a PostgreSQL database table using the `COPY` command.

6. **Spark Submit Task:** Submits a Spark application for additional data processing or analysis. This is done using bash operator

7. **Read Postgres Data:** Retrieves data from the PostgreSQL database table for further analysis.

8. **Display Postgres Data:** Displays the retrieved data from PostgreSQL in the Airflow logs.

##screenshots

1. postgres connection
   ![Screenshot from 2023-09-21 10-13-40](https://github.com/ssadichhya/airflow_project/assets/141208089/3f6aeaa2-78a2-4f7d-a9b4-9c0387ca2e9d)
2. Http connection
   ![image](https://github.com/ssadichhya/airflow_project/assets/141208089/f1e5f114-44a0-4e1d-8f11-66ee84a2211e)
3. DAG log displaying data read from postgres
   ![image](https://github.com/ssadichhya/airflow_project/assets/141208089/149e0a85-ba87-4de5-a83d-74d35bc80925)

## Prerequisites

Before running this DAG, make sure you have the following prerequisites installed and configured:

- Apache Airflow
- PostgreSQL database
- Spark (if using the Spark Submit Task)
- Necessary Python libraries and dependencies

## Installation

1. Clone this repository to your local machine or Airflow server:

