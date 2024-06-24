import psycopg2 as sql
from prettytable import PrettyTable
import json


def create_connection(
    db_name, db_user, db_password, db_host="localhost", db_port="5432"
):
    try:
        conn = sql.connect(
            dbname=db_name,
            user=db_user,
            password=db_password,
            host=db_host,
            port=db_port,
        )
        print(f"Соединение с базой данных '{db_name}' прошло успешно.")
        return conn
    except sql.OperationalError as e:
        Exception(f"Ошибка при соединении с базой данных '{db_name}': {e}")
        return None


class db_controller:
    def __init__(
        self,
        host="localhost",
        port=5432,
        dbname="tgsaler",
        user="tgsaler",
        password="tgsalerbot",
    ) -> None:
        # Параметры подключения к базе данных
        try:
            self.conn_string = (
                f"dbname={dbname} user={user} password={password} host={host} port={port}"
            )
        except Exception:
            print("Connection failed")
            print("You need to create database first")
            print("Run command: tgsalerdatabase")

    def get_user_by_id(self, user_id):
        # Укажите ваши данные для подключения к базе данных
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()

        try:
            # Выполняем SQL запрос для получения данных
            column_names = ["id", "tgid", "prev", "bin", "price"]
            cursor.execute("SELECT * FROM users WHERE tgid = %s;", (user_id,))
            user = cursor.fetchone()
            # print(dict(zip(column_names, user)))
            # Возвращаем результат в виде словаря
            return dict(zip(column_names, user)) if user else None

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

    def get_all_by_category(self, category_id):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()
        # print('aboba')
        # Определение столбцов таблицы products
        column_names = ["id", "name", "category", "price", "currency", "descr", "photo"]

        select_data_query = f"SELECT * FROM product WHERE category = '{category_id}';"
        cursor.execute(select_data_query, (category_id,))
        rows = cursor.fetchall()

        # Преобразование строк в массив словарей
        result = [dict(zip(column_names, row)) for row in rows]

        # Закрытие соединения
        cursor.close()
        conn.close()

        return result

    def get_product_data(self, name):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()
        column_names = ["id", "name", "category", "price", "currency", "descr", "photo"]
        select_data_query = f"SELECT * FROM product WHERE name = '{name}';"
        cursor.execute(select_data_query, (name,))
        row = cursor.fetchone()
        # Преобразование строк в массив словарей
        result = dict(zip(column_names, row))

        # Закрытие соединения
        cursor.close()
        conn.close()

        return result

    def get_categories(self):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        select_data_query = f"SELECT id, name FROM category;"
        cursor.execute(select_data_query)
        rows = cursor.fetchall()

        # Закрытие соединения
        cursor.close()
        conn.close()
        return rows

    def add_product(self, name, category, price, currency, descr="", photo=""):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()
        select_data_query = f"""SELECT * from category WHERE name = '{category}';"""
        # выполнение запроса
        cursor.execute(select_data_query)
        rows = cursor.fetchall()
        # print(rows)
        select_data_query = f"""INSERT INTO product(name, category, price, currency, descr, photo) VALUES ('{name}', '{rows[0][0]}', '{price}', '{currency}','{descr}', '{photo}');"""
        # выполнение запроса
        cursor.execute(select_data_query)
        conn.commit()
        cursor.close()
        conn.close()
        return None

    def add_category(self, name):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        select_data_query = f"""INSERT INTO category(name) VALUES ('{name}');"""
        # выполнение запроса
        cursor.execute(select_data_query)
        # rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        # rows = cursor.fetchall()
        return None

    def add_user(self, tgid):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        try:
            # Проверка существования пользователя с заданным tgid
            check_user_query = "SELECT 1 FROM users WHERE tgid = %s;"
            cursor.execute(check_user_query, (tgid,))
            user_exists = cursor.fetchone() is not None

            if not user_exists:
                # Если пользователя нет, выполняем вставку
                insert_user_query = "INSERT INTO users(tgid, price) VALUES (%s, 0);"
                cursor.execute(insert_user_query, (tgid,))
                conn.commit()
                print(f"User with tgid {tgid} added successfully.")
            else:
                print(f"User with tgid {tgid} already exists.")

        except Exception as e:
            print(f"An error occurred: {e}")
            conn.rollback()

        finally:
            cursor.close()
            conn.close()

        return None

    def edit_user_by_data(self, data):
        # Укажите ваши данные для подключения к базе данных
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()

        try:
            # Выполняем SQL запрос для получения данных
            cursor.execute(
                f"""UPDATE users SET prev = '{data['prev']}', bin = '{json.dumps(data['bin'])}', price = '{data['price']}' WHERE tgid = '{data['tgid']}';"""
            )
            connection.commit()
            # Возвращаем результат в виде словаря
            return 1

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

    def del_category(self, name):
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()
        cursor.execute(f"""DELETE FROM category WHERE name = '{name}';""")
        connection.commit()
        cursor.close()
        connection.close()

    def del_product(self, name):
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()
        cursor.execute(f"""DELETE FROM product WHERE name = '{name}';""")
        connection.commit()
        cursor.close()
        connection.close()

    def edit_produt_by_data(self, data):
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()

        try:
            # Выполняем SQL запрос для получения данных
            cursor.execute(
                f"""UPDATE product SET price = '{data['price']}', descr = '{data['descr']}', currency = '{data['currency']}', photo = '{data['photo']}', category = '{data['category']}'  WHERE name = '{data['name']}';"""
            )
            connection.commit()
            # Возвращаем результат в виде словаря
            return 1

        except Exception as e:
            print(f"An error occurred: {e}")
            return None

        finally:
            cursor.close()
            connection.close()

    def show_product(self):
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM product")
        table = PrettyTable()
        rows = cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        table.field_names = headers
        for row in rows:
            table.add_row(row)
        cursor.close()
        connection.close()
        return table

    def show_category(self):
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()
        cursor.execute("SELECT * FROM category")
        table = PrettyTable()
        rows = cursor.fetchall()
        headers = [column[0] for column in cursor.description]
        table.field_names = headers
        for row in rows:
            table.add_row(row)
        cursor.close()
        connection.close()
        return table
