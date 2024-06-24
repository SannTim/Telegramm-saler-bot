"""Модуль, реализующий запросы к бд."""

import psycopg2 as sql
from prettytable import PrettyTable
import json


def create_connection(
    db_name, db_user, db_password, db_host="localhost", db_port="5432"
):
    """
    Эта функция соединяется с базой данных.

    :param str db_name: Имя базы данных
    :param str db_user: Имя пользователя базы данных
    :param str db_password: Пароль пользователя базы данных
    :param str db_host: Хост базы данных (по умолчанию "localhost")
    :param str db_port: Порт базы данных (по умолчанию "5432")
    :return: Объект соединения
    :rtype: sql.connection
    """
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
    """Класс для совершения манипуляций с базой данных."""

    def __init__(
        self,
        host="localhost",
        port=5432,
        dbname="tgsaler",
        user="tgsaler",
        password="tgsalerbot",
    ) -> None:
        """
        Инициализация контроллера базы данных.

        :param str host: Хост базы данных
        :param int port: Порт базы данных
        :param str dbname: Имя базы данных
        :param str user: Имя пользователя базы данных
        :param str password: Пароль пользователя базы данных
        """
        # Параметры подключения к базе данных
        try:
            self.conn_string = f"dbname={dbname} user={user} password={password} host={host} port={port}"
        except Exception:
            print("Connection failed")
            print("You need to create database first")
            print("Run command: tgsalerdatabase")

    def get_user_by_id(self, user_id):
        """
        Получает информацию о пользователе по его идентификатору.

        :param int user_id: Идентификатор пользователя
        :return: Информация о пользователе в виде словаря
        :rtype: dict
        """
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
        """
        Получает все продукты по их категории.

        :param str category_id: Идентификатор категории
        :return: Список продуктов в виде массива словарей
        :rtype: list
        """
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
        """
        Получает данные о продукте по его имени.

        :param str name: Имя продукта
        :return: Данные о продукте в виде словаря
        :rtype: dict
        """
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
        """
        Получает все категории продуктов.

        :return: Список категорий в виде массива кортежей
        :rtype: list
        """
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        select_data_query = "SELECT id, name FROM category;"
        cursor.execute(select_data_query)
        rows = cursor.fetchall()

        # Закрытие соединения
        cursor.close()
        conn.close()
        return rows

    def add_product(self, name, category, price, currency, descr="", photo=""):
        """
        Добавляет новый продукт.

        :param str name: Имя продукта
        :param str category: Категория продукта
        :param float price: Цена продукта
        :param str currency: Валюта
        :param str descr: Описание (по умолчанию "")
        :param str photo: Фото (по умолчанию "")
        :return: None
        :rtype: None
        """
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()
        select_data_query = f"""SELECT * from category WHERE name = '{
            category}';"""
        # выполнение запроса
        cursor.execute(select_data_query)
        rows = cursor.fetchall()
        # print(rows)
        select_data_query = f"""INSERT INTO product(name, category, price, currency, descr, photo) VALUES ('{
            name}', '{rows[0][0]}', '{price}', '{currency}','{descr}', '{photo}');"""
        # выполнение запроса

        cursor.execute(select_data_query)

        conn.commit()
        # print(select_data_query)
        cursor.close()
        conn.close()

        return None

    def add_category(self, name):
        """
        Добавляет новую категорию.

        :param str name: Имя категории
        :return: None
        :rtype: None
        """
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        select_data_query = f"""INSERT INTO category(name) VALUES ('{
            name}');"""
        # выполнение запроса
        cursor.execute(select_data_query)
        # rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        # rows = cursor.fetchall()
        return None

    def add_user(self, tgid):
        """
        Добавляет нового пользователя.

        :param int tgid: Telegram ID пользователя
        :return: None
        :rtype: None
        """
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
        """
        Редактирует данные пользователя.

        :param dict data: Данные пользователя для редактирования
        :return: Результат редактирования (1 - успешно, None - неудача)
        :rtype: int
        """
        # Укажите ваши данные для подключения к базе данных
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()

        try:
            # Выполняем SQL запрос для получения данных
            cursor.execute(
                f"""UPDATE users SET prev = '{data['prev']}', bin = '{json.dumps(
                    data['bin'])}', price = '{data['price']}' WHERE tgid = '{data['tgid']}';"""
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
        """
        Удаляет категорию.

        :param str name: Имя категории
        """
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()
        cursor.execute(f"""DELETE FROM category WHERE name = '{name}';""")
        connection.commit()
        cursor.close()
        connection.close()

    def del_product(self, name):
        """
        Удаляет продукт.

        :param str name: Имя продукта
        """
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()
        cursor.execute(f"""DELETE FROM product WHERE name = '{name}';""")
        connection.commit()
        cursor.close()
        connection.close()

    def edit_produt_by_data(self, data):
        """
        Редактирует данные о продукте.

        :param dict data: Данные о продукте для редактирования
        :return: Результат редактирования (1 - успешно, None - неудача)
        :rtype: int
        """
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor()

        try:
            # Выполняем SQL запрос для получения данных
            cursor.execute(
                f"""UPDATE product SET price = '{data['price']}', descr = '{data['descr']}', currency = '{
                    data['currency']}', photo = '{data['photo']}', category = '{data['category']}'  WHERE name = '{data['name']}';"""
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
        """
        Возвращает таблицу всех продуктов.

        :return: Таблица продуктов
        :rtype: PrettyTable
        """
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
        """
        Возвращает таблицу всех категорий.

        :return: Таблица категорий
        :rtype: PrettyTable
        """
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
