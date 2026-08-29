import configparser
import pathlib
import psycopg2
from psycopg2 import sql
import csv
import sys
from airflow.hooks.base import BaseHook

"""
Download Redshift table to CSV file. Will be stored under /tmp folder.
"""

# Parse configuration file
script_path = pathlib.Path(__file__).parent.resolve()
parser = configparser.ConfigParser()
parser.read(f"{script_path}/configuration.conf")

# Store configuration variables
redshift_conn = BaseHook.get_connection("redshift_dbt")
USERNAME = redshift_conn.login
PASSWORD = redshift_conn.password
HOST = redshift_conn.host
PORT = redshift_conn.port
DATABASE = redshift_conn.schema
TABLE_NAME = 'fct_posts'
SCHEMA_NAME = 'marts'


# TODO Improve error handling
def connect_to_redshift():
    """Connect to Redshift instance"""
    try:
        rs_conn = psycopg2.connect(
            dbname=DATABASE, user=USERNAME, password=PASSWORD, host=HOST, port=PORT
        )
        return rs_conn
    except Exception as e:
        print(f"Unable to connect to Redshift. Error {e}")
        sys.exit(1)

# TODO Error handling
def download_redshift_data(rs_conn):
    """Download data from Redshift table to CSV"""
    with rs_conn:
        cur = rs_conn.cursor()
        cur.execute(
            sql.SQL("SELECT * FROM {db}.{schema}.{table};").format(table=sql.Identifier(TABLE_NAME),db=sql.Identifier(DATABASE),schema=sql.Identifier(SCHEMA_NAME))
        )
        result = cur.fetchall()
        headers = [col[0] for col in cur.description]
        result.insert(0, tuple(headers))
        fp = open("/opt/airflow/data_staging/redshift_fct_posts.csv", "w")
        myFile = csv.writer(fp)
        myFile.writerows(result)
        fp.close()


if __name__ == "__main__":
    rs_conn = connect_to_redshift()
    download_redshift_data(rs_conn)
