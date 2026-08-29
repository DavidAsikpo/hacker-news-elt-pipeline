FROM apache/airflow:2.10.4-python3.11

USER root

RUN python -m venv /opt/dbt_venv && \
    PIP_USER=false /opt/dbt_venv/bin/pip install --no-cache-dir dbt-redshift==1.11.1 && \
    chown -R airflow:root /opt/dbt_venv

USER airflow
RUN PIP_USER=false pip install --no-cache-dir astronomer-cosmos==1.9.0