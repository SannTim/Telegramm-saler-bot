import psycopg2 as sql


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
    def __init__(self) -> None:
        # Параметры подключения к базе данных
        dbname = "tgsaler"
        user = "tgsaler"
        password = "tgsalerbot"
        host = "localhost"
        port = 5432
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

    def add_product(self, name, category, price, currency):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()
        select_data_query = f"""SELECT * from category WHERE name = '{category}'"""
        # выполнение запроса
        cursor.execute(select_data_query)
        rows = cursor.fetchall()
        select_data_query = f"""INSERT INTO product(name, category, price, currency) VALUES ('{name}', '{rows[0][0]}', '{price}', '{currency}')"""
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

        select_data_query = f"""INSERT INTO category(name) VALUES ('{name}')"""
        # выполнение запроса
        cursor.execute(select_data_query)
        # rows = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        # rows = cursor.fetchall()
        return None
