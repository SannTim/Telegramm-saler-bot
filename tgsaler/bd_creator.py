from typing import ParamSpecArgs
import psycopg2
from psycopg2 import sql, OperationalError
import sys

# Подключение к PostgreSQL

if len(sys.argv) > 1:
    user = sys.argv[1]
    password = ""
    host = "localhost"

    if len(sys.argv) > 2:
        password = sys.argv[2]
    if len(sys.argv) > 3:
        host = sys.argv[3]

else:
    user = input("Enter username\n>")
    password = input("Enter password\n>")
    host = input("Enter host\n>")


def create_connection(db_name, db_user, db_password, db_host):
    try:
        conn = psycopg2.connect(
            dbname=db_name, user=db_user, password=db_password, host=db_host
        )
        print(f"Соединение с базой данных '{db_name}' прошло успешно.")
        return conn
    except OperationalError as e:
        print(f"Ошибка при соединении с базой данных '{db_name}': {e}")
        return None


# Подключение к PostgreSQL
conn = create_connection("postgres", user, password, host)

if conn:
    conn.autocommit = True
    cur = conn.cursor()

    # Создание базы данных
    try:
        cur.execute("DROP DATABASE IF EXISTS tgsaler")
        cur.execute("CREATE DATABASE tgsaler")
        print("База данных 'tgsaler' успешно создана.")
    except Exception as e:
        print(f"Ошибка при создании базы данных 'tgsaler': {e}")

    # Подключение к базе данных tgsaler
    conn.close()
    conn = create_connection("tgsaler", user, password, host)

    if conn:
        cur = conn.cursor()

        # Создание таблицы категорий
        try:
            cur.execute(
                """
                CREATE TABLE category (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL
                )
            """
            )
            print("Таблица 'category' успешно создана.")
        except Exception as e:
            print(f"Ошибка при создании таблицы 'category': {e}")

        # Создание таблицы продуктов
        try:
            cur.execute(
                """
                CREATE TABLE product (
                    id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    category INTEGER NOT NULL REFERENCES category(id),
                    price DECIMAL(10, 2) NOT NULL,
                    currency VARCHAR(3) NOT NULL
                )
            """
            )
            print("Таблица 'product' успешно создана.")
        except Exception as e:
            print(f"Ошибка при создании таблицы 'product': {e}")

        # Создание таблицы пользователей
        try:
            cur.execute(
                """
                CREATE TABLE users (
                    id SERIAL PRIMARY KEY,
                    tgid BIGINT NOT NULL,
                    prev TEXT
                )
            """
            )
            print("Таблица 'users' успешно создана.")
        except Exception as e:
            print(f"Ошибка при создании таблицы 'users': {e}")

        # Создание роли tgsaler и предоставление привилегий
        try:
            role_password = "tgsalerbot"
            cur.execute(
                sql.SQL("CREATE ROLE tgsaler WITH LOGIN PASSWORD %s"), [role_password]
            )
            cur.execute("GRANT ALL PRIVILEGES ON DATABASE tgsaler TO tgsaler")
            cur.execute(
                "GRANT ALL PRIVILEGES ON ALL TABLES IN SCHEMA public TO tgsaler"
            )
            cur.execute(
                "GRANT ALL PRIVILEGES ON ALL SEQUENCES IN SCHEMA public TO tgsaler"
            )
            print("Роль 'tgsaler' успешно создана и привилегии предоставлены.")
        except Exception as e:
            print(
                f"Ошибка при создании роли 'tgsaler' или предоставлении привилегий: {e}"
            )

        # Закрытие соединения
        conn.commit()
        cur.close()
        conn.close()
        print("Соединение закрыто.")
else:
    print("Не удалось подключиться к базе данных 'postgres'.")
