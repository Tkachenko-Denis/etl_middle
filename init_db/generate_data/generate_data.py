import random
import os
import string
from datetime import datetime, timedelta
import psycopg2

# Конфигурация подключения к базе данных
def get_db_connection():
    return psycopg2.connect(
        dbname=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT", 5432)
    )

# Функция для генерации случайного имени

def random_name(length=8):
    return ''.join(random.choices(string.ascii_letters, k=length)).capitalize()

# Функция для генерации случайного email

def random_email():
    domains = ["gmail.com", "yahoo.com", "hotmail.com"]
    return f"{random_name(5).lower()}{random.randint(100, 999)}@{random.choice(domains)}"

# Функция для генерации случайного номера телефона

def random_phone():
    return f"+{random.randint(1, 99)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"

# Генерация данных для таблиц Users
def generate_users(cursor, count=100):
    for _ in range(count):
        first_name = random_name()
        last_name = random_name()
        email = random_email()
        phone = random_phone()
        registration_date = datetime.now() - timedelta(days=random.randint(0, 1000))
        loyalty_status = random.choice(["Bronze", "Silver", "Gold", "Platinum"])
        cursor.execute(
            """
            INSERT INTO Users (first_name, last_name, email, phone, registration_date, loyalty_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (first_name, last_name, email, phone, registration_date, loyalty_status)
        )

# Генерация данных для таблицы ProductCategories
def generate_product_categories(cursor, count=10):
    for _ in range(count):
        name = random_name(10)
        parent_category_id = random.choice([None] + list(range(1, count // 2)))
        cursor.execute(
            """
            INSERT INTO ProductCategories (name, parent_category_id)
            VALUES (%s, %s)
            """,
            (name, parent_category_id)
        )

# Генерация данных для таблицы Products
def generate_products(cursor, count=50):
    for _ in range(count):
        name = random_name(12)
        description = "This is a description of " + name
        category_id = random.randint(1, 10)
        price = round(random.uniform(5, 500), 2)
        stock_quantity = random.randint(1, 100)
        creation_date = datetime.now() - timedelta(days=random.randint(0, 1000))
        cursor.execute(
            """
            INSERT INTO Products (name, description, category_id, price, stock_quantity, creation_date)
            VALUES (%s, %s, %s, %s, %s, %s)
            """,
            (name, description, category_id, price, stock_quantity, creation_date)
        )

# Генерация данных для таблицы Orders и OrderDetails
def generate_orders_and_details(cursor, user_count=100, product_count=50, order_count=200):
    for _ in range(order_count):
        user_id = random.randint(1, user_count)
        order_date = datetime.now() - timedelta(days=random.randint(0, 100))
        status = random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
        delivery_date = (order_date + timedelta(days=random.randint(1, 14))) if status != "Pending" else None

        # Вставка заказа
        cursor.execute(
            """
            INSERT INTO Orders (user_id, order_date, total_amount, status, delivery_date)
            VALUES (%s, %s, 0, %s, %s)
            RETURNING order_id
            """,
            (user_id, order_date, status, delivery_date)
        )
        order_id = cursor.fetchone()[0]

        # Генерация деталей заказа
        total_amount = 0
        for _ in range(random.randint(1, 5)):
            product_id = random.randint(1, product_count)
            quantity = random.randint(1, 10)
            cursor.execute("SELECT price FROM Products WHERE product_id = %s", (product_id,))
            price_per_unit = cursor.fetchone()[0]
            total_price = price_per_unit * quantity
            total_amount += total_price

            cursor.execute(
                """
                INSERT INTO OrderDetails (order_id, product_id, quantity, price_per_unit, total_price)
                VALUES (%s, %s, %s, %s, %s)
                """,
                (order_id, product_id, quantity, price_per_unit, total_price)
            )

        # Обновление суммы заказа
        cursor.execute(
            """
            UPDATE Orders SET total_amount = %s WHERE order_id = %s
            """,
            (total_amount, order_id)
        )

# Основной блок выполнения
if __name__ == "__main__":
    try:
        conn = get_db_connection()
        cursor = conn.cursor()

        generate_users(cursor, 100)
        generate_product_categories(cursor, 10)
        generate_products(cursor, 50)
        generate_orders_and_details(cursor, 100, 50, 200)

        conn.commit()
        print("Data generation completed successfully!")

    except Exception as e:
        print("An error occurred:", e)
        if conn:
            conn.rollback()

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
