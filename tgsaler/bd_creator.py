from typing import ParamSpecArgs
import psycopg2
from psycopg2 import sql, OperationalError
import sys
# Подключение к PostgreSQL

if len(sys.argv) == 3:
    user = sys.argv[1]
    password = sys.argv[2]
    host = sys.argv[3]
else:
    user = input('Enter username\n>')
    password = input('Enter password\n>')
    host = input('Enter host\n>')


def create_connection(db_name, db_user, db_password, db_host):
    try:
        conn = psycopg2.connect(dbname=db_name, user=db_user, password=db_password, host=db_host)
        print(f"Соединение с базой данных '{db_name}' прошло успешно.")
        return conn
    except OperationalError as e:
        print(f"Ошибка при соединении с базой данных '{db_name}': {e}")
        return None


# Подключение к PostgreSQL
conn = create_connection("postgres", user, password, host)
conn.autocommit = True
cur = conn.cursor()

# Создание базы данных
cur.execute("DROP DATABASE IF EXISTS tgsaler")
cur.execute("CREATE DATABASE tgsaler")

# Подключение к базе данных tgsaler
conn.close()
conn = psycopg2.connect(dbname="tgsaler", user="your_username", password="your_password", host="localhost")
cur = conn.cursor()

# Создание таблицы категорий
cur.execute("""
    CREATE TABLE category (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL
    )
""")

# Создание таблицы продуктов
cur.execute("""
    CREATE TABLE product (
        id SERIAL PRIMARY KEY,
        name VARCHAR(255) NOT NULL,
        category INTEGER NOT NULL REFERENCES category(id),
        price DECIMAL(10, 2) NOT NULL,
        currency VARCHAR(3) NOT NULL
    )
""")

# Создание таблицы пользователей
cur.execute("""
    CREATE TABLE users (
        id SERIAL PRIMARY KEY,
        tgid BIGINT NOT NULL,
        prev TEXT
    )
""")

# Закрытие соединения
conn.commit()
cur.close()
conn.close()

print("База данных и таблицы успешно созданы.")

