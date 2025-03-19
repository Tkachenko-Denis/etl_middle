# Используем базовый образ с Python
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /app

# Копируем файлы проекта в контейнер
COPY ./generate_data_for_kafka/generate_data_for_kafka.py /app/generate_data_for_kafka.py
COPY requirements.txt /app/requirements.txt

# Устанавливаем зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Устанавливаем точку входа
ENTRYPOINT ["python", "/app/generate_data_for_kafka.py"]
