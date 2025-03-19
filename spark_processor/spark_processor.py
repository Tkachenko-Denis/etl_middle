from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col
from pyspark.sql.types import StructType, StructField, IntegerType, StringType, FloatType, TimestampType, DateType
import psycopg2

# Определяем схему данных
schema = StructType([
    StructField("order_id", IntegerType(), True),
    StructField("user_id", IntegerType(), True),
    StructField("order_date", TimestampType(), True),
    StructField("total_amount", FloatType(), True),
    StructField("status", StringType(), True),
    StructField("delivery_date", DateType(), True),
])

# Spark сессия
spark = SparkSession.builder \
    .appName("KafkaToPostgres") \
    .getOrCreate()

# Чтение данных из Kafka
df = spark.readStream \
    .format("kafka") \
    .option("kafka.bootstrap.servers", "kafka:9092") \
    .option("subscribe", "orders") \
    .load()

# Декодируем сообщение из Kafka
orders = df.select(from_json(col("value").cast("string"), schema).alias("data")).select("data.*")

# Функция для записи в PostgreSQL
def write_to_postgres(batch_df, batch_id):
    batch_df.write \
        .format("jdbc") \
        .option("url", "jdbc:postgresql://postgres:5432/source_db") \
        .option("dbtable", "orders") \
        .option("user", "admin") \
        .option("password", "admin") \
        .mode("append") \
        .save()

# Запуск обработки
orders.writeStream \
    .foreachBatch(write_to_postgres) \
    .start() \
    .awaitTermination()

