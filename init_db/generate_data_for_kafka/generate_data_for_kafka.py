import json
import random
from datetime import datetime, timedelta
from kafka import KafkaProducer

# Настройка Kafka
producer = KafkaProducer(
    bootstrap_servers='kafka:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TOPIC = "orders"

# Генерация данных
def generate_order_data():
    order_id = random.randint(1000, 9999)
    user_id = random.randint(1, 100)
    order_date = datetime.now()
    total_amount = round(random.uniform(10.0, 500.0), 2)
    status = random.choice(["Pending", "Shipped", "Delivered", "Cancelled"])
    delivery_date = (order_date + timedelta(days=random.randint(1, 7))).date()

    return {
        "order_id": order_id,
        "user_id": user_id,
        "order_date": order_date.isoformat(),
        "total_amount": total_amount,
        "status": status,
        "delivery_date": str(delivery_date),
    }

# Отправка данных в Kafka
for _ in range(100):  # Генерация 100 заказов
    order_data = generate_order_data()
    producer.send(TOPIC, order_data)
    print(f"Sent: {order_data}")

