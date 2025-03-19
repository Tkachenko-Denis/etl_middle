# Практическая работа по предмету ETL

Этот репозиторий содержит проект конвейера обработки данных, включающий генерацию данных, публикацию через Kafka, обработку Spark'ом и сохранение в базу данных PostgreSQL. Также используется Airflow для оркестрации процессов репликации данных из PostgreSQL в MySQL и создания аналитических витрин.

---

## Общие требования

- Все сервисы контейнеризованы с использованием Docker и настроены для работы в изолированной среде.
- Все зависимости для Python-сервисов описаны в `requirements.txt`.
- Компоненты легко масштабируемы и совместимы между собой.

---

## Компоненты проекта

### PostgreSQL
- Хранит первичные данные.
- Инициализируется таблицами и тестовыми данными из файла `init_db/init_postgres.sql`.

### MySQL
- Альтернативная база данных, используемая для репликации данных и аналитических витрин.
- Инициализируется таблицами и тестовыми данными из файла `init_db/init_mysql.sql`.

### Zookeeper и Kafka
- **Zookeeper** управляет координацией Kafka.
- **Kafka** обрабатывает события и публикует сообщения в топике `orders`.

### Data Generator
- Генерация данных:
  - `generate_data.py`: записывает данные непосредственно в PostgreSQL.
  - `generate_data_for_kafka.py`: публикует данные в Kafka.

### Spark
- **Spark Master** управляет обработкой данных.
- **Spark Processor (`spark_processor.py`)**:
  - Читает сообщения из Kafka.
  - Обрабатывает их и записывает в PostgreSQL.

### Apache Airflow
- Оркестрация и управление потоками данных.

---

## Установка и запуск

### Скачивание
Клонируйте репозиторий:

```bash
git clone https://github.com/Tkachenko-Denis/python_final
cd python_final
```
### Сборка и запуск

```bash
docker-compose up --build
```
### Доступ к сервисам:

- PostgreSQL: `localhost:5432` (логин: `admin`, пароль: `admin`)
- MySQL: `localhost:3306` (логин: `user`, пароль: `password`)
- Kafka: `localhost:9092`
- Airflow: `http://localhost:8080` (логин: `admin`, пароль: `admin`)


## Структура проекта

```plaintext
project/
├── dags/                            # DAG-файлы для Airflow
│   └── create_data_marts.py
│   └──postgres_to_mysql.py
├── init_db/                         # Скрипты инициализации баз данных
│   ├── init_postgres.sql
│   ├── init_mysql.sql
├── generate_data/                   # Генерация данных для PostgreSQL
│   ├── Dockerfile
│   ├── generate_data.py
├── generate_data_for_kafka/         # Генерация данных для Kafka
│   ├── Dockerfile
│   ├── generate_data_for_kafka.py
├── spark_processor/                 # Обработка данных из Kafka в Spark
│   ├── Dockerfile
│   ├── spark_processor.py
├── requirements.txt                 # Зависимости для всех Python-компонентов
├── docker-compose.yml               # Конфигурация Docker Compose
└── README.md                        # Документация проекта
```

---

## Аналитическая витрина: UserOrders

### Описание  
Витрина `UserOrders` предназначена для анализа активности пользователей, включая количество их заказов, общую сумму потраченных средств и дату последнего заказа. Это позволяет оценить вовлечённость пользователей, их покупательскую активность и историю взаимодействий с системой.

### Поля и их описание  

| Поле              | Описание                                 |
|-------------------|------------------------------------------|
| `user_id`         | Уникальный идентификатор пользователя    |
| `total_orders`    | Общее количество заказов пользователя    |
| `total_amount`    | Общая сумма потраченных средств          |
| `last_order_date` | Дата последнего заказа пользователя      |

### Логика формирования  

1. **Источник данных**:  
   - Таблица `Users` для получения списка пользователей.
   - Таблица `Orders` для расчёта активности пользователей.

2. **Алгоритм расчёта**:
   - Подсчёт количества заказов для каждого пользователя (`COUNT(o.order_id)`).
   - Сумма всех заказов для каждого пользователя (`SUM(o.total_amount)`).
   - Дата последнего заказа пользователя (`MAX(o.order_date)`).
   - Пользователи, не имеющие заказов, получают значения `0` для суммы заказов (`COALESCE`).

3. **Очистка перед вставкой**:  
   Перед обновлением данных в таблице выполняется очистка (`TRUNCATE TABLE UserOrders`), чтобы избежать дублирования записей.

4. **Обновление данных**:  
   Данные вставляются с использованием запроса `INSERT INTO ... SELECT`, который собирает информацию из исходных таблиц.

### Применение  
- Оценка покупательской активности пользователей.
- Анализ истории взаимодействия с клиентами.
- Создание сегментации пользователей по количеству и общей сумме заказов.

## Аналитическая витрина: ProductSales

### Описание  
Витрина `ProductSales` предназначена для анализа продаж продуктов, включая количество проданных единиц и общую выручку. Она помогает определить популярность товаров, их вклад в общий доход и оценить эффективность продаж.

### Поля и их описание  

| Поле             | Описание                                   |
|------------------|--------------------------------------------|
| `product_id`     | Уникальный идентификатор товара            |
| `total_sold`     | Общее количество проданных единиц товара   |
| `total_revenue`  | Общая выручка от продаж товара             |

### Логика формирования  

1. **Источник данных**:  
   - Таблица `OrderDetails` используется для подсчёта количества и суммы продаж для каждого товара.

2. **Алгоритм расчёта**:
   - Подсчёт общего количества проданных единиц товара (`SUM(od.quantity)`).
   - Сумма общей выручки от продаж товара (`SUM(od.total_price)`).
   - Группировка данных по идентификатору товара (`GROUP BY od.product_id`).

3. **Очистка перед вставкой**:  
   Перед обновлением данных в таблице выполняется очистка (`TRUNCATE TABLE ProductSales`), чтобы избежать дублирования записей.

4. **Обновление данных**:  
   Данные вставляются с использованием запроса `INSERT INTO ... SELECT`, который агрегирует информацию из таблицы `OrderDetails`.

### Применение  
- Анализ популярности товаров по количеству продаж.
- Оценка выручки от каждого товара.
- Поддержка принятия решений о стратегиях закупок и маркетинга.
