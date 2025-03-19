# Используем базовый образ Spark
FROM bitnami/spark:latest

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./spark_processor/spark_processor.py /app/spark_processor.py
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r /app/requirements.txt

# Команда запуска Spark
CMD ["spark-submit", "--master", "local[*]", "/app/spark_processor.py"]

