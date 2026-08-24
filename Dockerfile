FROM apache/airflow:2.8.1

# Install Cosmos + dbt adapter in an isolated venv to avoid dependency conflicts with Airflow's own packages
RUN python -m venv /opt/dbt_venv && \
    /opt/dbt_venv/bin/pip install --no-cache-dir dbt-redshift

USER airflow
RUN pip install --no-cache-dir astronomer-cosmos==1.4.3

