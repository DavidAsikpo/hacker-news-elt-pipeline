from os import remove
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.utils.dates import days_ago
from datetime import timedelta, datetime
from cosmos import DbtTaskGroup, ProjectConfig, ProfileConfig, ExecutionConfig, ExecutionMode
from cosmos.profiles import RedshiftUserPasswordProfileMapping

"""
DAG to extract Reddit data, load into AWS S3, and copy to AWS Redshift
"""

# Output name of extracted file. This be passed to each
# DAG task so they know which file to process
output_name = datetime.now().strftime("%Y%m%d")

# Run our DAG daily and ensures DAG run will kick off
# once Airflow is started, as it will try to "catch up"
schedule_interval = "@daily"
start_date = datetime(2026, 8, 24) # Start date for DAG run. This will be used to "catch up" and run DAG for each day since this date

default_args = {"owner": "David", "depends_on_past": False, "retries": 1}

profile_config = ProfileConfig(
    profile_name="hackstories_dbt",
    target_name="dev",
    profile_mapping=RedshiftUserPasswordProfileMapping(
        conn_id="redshift_dbt",  # set this up as an Airflow Connection
        profile_args={"schema": "public"},
    ),
)

execution_config = ExecutionConfig(
    execution_mode = ExecutionMode.LOCAL,
    dbt_executable_path = "/opt/dbt_venv/bin/dbt"
)

with DAG(
    dag_id="elt_hackstories_pipeline",
    description="hackstories ELT",
    schedule_interval=schedule_interval,
    default_args=default_args,
    start_date=start_date,
    catchup=False,
    max_active_runs=1,
    tags=["hackstoriesETL"],
) as dag:

    extract_hackstories_data = BashOperator(
        task_id="extract_hackstories_data",
        bash_command=f"python /opt/airflow/extraction/extract_hackstories_etl.py {output_name}",
        dag=dag,
    )
    extract_hackstories_data.doc_md = "Extract hackstories data and store as CSV"

    upload_to_s3 = BashOperator(
        task_id="upload_to_s3",
        bash_command=f"python /opt/airflow/extraction/upload_aws_s3_etl.py {output_name}",
        dag=dag,
    )
    upload_to_s3.doc_md = "Upload hackstories CSV data to S3 bucket"

    copy_to_redshift = BashOperator(
        task_id="copy_to_redshift",
        bash_command=f"python /opt/airflow/extraction/upload_aws_redshift_etl.py {output_name}",
        dag=dag,
    )
    copy_to_redshift.doc_md = "Copy S3 CSV file to Redshift table"

    dbt_transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=ProjectConfig("/opt/airflow/dbt"),
        profile_config=profile_config,
        execution_config=execution_config,
    )

    download_from_redshift = BashOperator(
        task_id="download_from_redshift",
        bash_command=f"python /opt/airflow/extraction/download_redshift_to_csv.py {output_name}",
        dag=dag,
    )
    download_from_redshift.doc_md = "Download data from Redshift table"


    

extract_hackstories_data >> upload_to_s3 >> copy_to_redshift >> dbt_transform >> download_from_redshift