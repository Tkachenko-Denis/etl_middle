FROM python:3.9-slim

# Установка зависимостей
RUN pip install psycopg2-binary

# Копирование скрипта в контейнер
WORKDIR /app
COPY ./generate_data/generate_data.py /app/generate_data.py

# Команда по умолчанию для запуска скрипта
CMD ["python", "/app/generate_data.py"]
