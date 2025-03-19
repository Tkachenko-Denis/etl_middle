from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import psycopg2
import pymysql
import logging

# Настройка логгирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def replicate_table(postgres_cursor, mysql_cursor, table_name):
    logger.info(f"Replicating table: {table_name}")
    postgres_cursor.execute(f'SELECT * FROM {table_name}')
    data = postgres_cursor.fetchall()
    columns = [desc[0] for desc in postgres_cursor.description]

    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    mysql_cursor.execute(f'DELETE FROM {table_name}')
    if data:
        mysql_cursor.executemany(
            f"INSERT INTO {table_name} ({', '.join(columns)}) VALUES ({', '.join(['%s']*len(columns))})",
            data
        )
    mysql_cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    logger.info(f"Table {table_name} replicated successfully.")

def replicate_data():
    try:
        postgres_conn = psycopg2.connect(
            dbname='source_db',
            user='admin',
            password='admin',
            host='postgres_container',
            port=5432
        )
        postgres_cursor = postgres_conn.cursor()

        mysql_conn = pymysql.connect(
            host='mysql_container',
            user='user',
            password='password',
            database='target_db',
            port=3306
        )
        mysql_cursor = mysql_conn.cursor()

        tables = ['Users', 'ProductCategories', 'Products', 'Orders', 'OrderDetails']
        for table in tables:
            replicate_table(postgres_cursor, mysql_cursor, table)

        mysql_conn.commit()

    except Exception as e:
        logger.error(f"Error during replication: {e}")
        if mysql_conn:
            mysql_conn.rollback()

    finally:
        if postgres_cursor:
            postgres_cursor.close()
        if postgres_conn:
            postgres_conn.close()
        if mysql_cursor:
            mysql_cursor.close()
        if mysql_conn:
            mysql_conn.close()

with DAG(
    'replicate_postgres_to_mysql',
    default_args={'retries': 1},
    description='Replicate data from PostgreSQL to MySQL',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:
    replicate_task = PythonOperator(
        task_id='replicate_data',
        python_callable=replicate_data
    )
    replicate_task

