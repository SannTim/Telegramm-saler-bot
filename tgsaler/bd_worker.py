import psycopg2 as sql
from . import functionals


class db_controller:
    def __init__(self, dbinfofile) -> None:
        properties = functionals.ini_to_dict(file_path=dbinfofile)
        # Параметры подключения к базе данных
        dbname = properties["dbname"]
        user = properties["user"]
        password = properties["password"]
        host = properties["host"]
        port = properties["port"]
        self.conn_string = (
            f"dbname={dbname} user={user} password={password} host={host} port={port}"
        )

    def get_all_by_category(self, category_id):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        select_data_query = f"SELECT * FROM products WHERE category = '{category_id}'"
        cursor.execute(select_data_query)
        rows = cursor.fetchall()

        # Закрытие соединения
        cursor.close()
        conn.close()
        return rows

    def add_product(self, name, category_id, price, currency):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        select_data_query = f"""INSERT INTO products(name, category, price, currency) VALUES ({name}, {category_id}, {price}, {currency})"""
    
