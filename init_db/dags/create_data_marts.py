from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pymysql

def create_user_orders_mart():
    # Подключение к MySQL
    conn = pymysql.connect(
        host='mysql_container',
        user='user',
        password='password',
        database='target_db',
        port=3306
    )
    cursor = conn.cursor()

    # Создание аналитической витрины UserOrders
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS UserOrders (
            user_id INT,
            total_orders INT,
            total_amount DECIMAL(10, 2),
            last_order_date DATE,
            PRIMARY KEY (user_id)
        )
    """)

    # Очистка таблицы перед вставкой (опционально)
    cursor.execute("TRUNCATE TABLE UserOrders")

    # Вставка или обновление данных в UserOrders
    cursor.execute("""
        INSERT INTO UserOrders (user_id, total_orders, total_amount, last_order_date)
        SELECT
            u.user_id,
            COUNT(o.order_id) AS total_orders,
            COALESCE(SUM(o.total_amount), 0) AS total_amount,
            MAX(o.order_date) AS last_order_date
        FROM Users u
        LEFT JOIN Orders o ON u.user_id = o.user_id
        GROUP BY u.user_id
    """)

    conn.commit()
    cursor.close()
    conn.close()

def create_product_sales_mart():
    # Подключение к MySQL
    conn = pymysql.connect(
        host='mysql_container',
        user='user',
        password='password',
        database='target_db',
        port=3306
    )
    cursor = conn.cursor()

    # Создание аналитической витрины ProductSales
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS ProductSales (
            product_id INT,
            total_sold INT,
            total_revenue DECIMAL(10, 2),
            PRIMARY KEY (product_id)
        )
    """)

    # Очистка таблицы перед вставкой (опционально)
    cursor.execute("TRUNCATE TABLE ProductSales")

    # Вставка данных в ProductSales
    cursor.execute("""
        INSERT INTO ProductSales (product_id, total_sold, total_revenue)
        SELECT
            od.product_id,
            SUM(od.quantity) AS total_sold,
            SUM(od.total_price) AS total_revenue
        FROM OrderDetails od
        GROUP BY od.product_id
    """)

    conn.commit()
    cursor.close()
    conn.close()

with DAG(
    'create_data_marts',
    default_args={'retries': 1},
    description='Create data marts in MySQL',
    schedule_interval='@daily',
    start_date=datetime(2025, 1, 1),
    catchup=False,
) as dag:
    create_user_orders = PythonOperator(
        task_id='create_user_orders_mart',
        python_callable=create_user_orders_mart
    )
    
    create_product_sales = PythonOperator(
        task_id='create_product_sales_mart',
        python_callable=create_product_sales_mart
    )

    create_user_orders >> create_product_sales
