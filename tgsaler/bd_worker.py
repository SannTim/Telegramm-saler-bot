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



    def get_user_by_id(self, user_id):
    # Укажите ваши данные для подключения к базе данных
        connection = sql.connect(self.conn_string)
        cursor = connection.cursor(cursor_factory=sql.RealDictCursor)

        try:
            # Выполняем SQL запрос для получения данных
            cursor.execute("SELECT * FROM users WHERE tgid = %s", (user_id,))
            user = cursor.fetchone()

            # Возвращаем результат в виде словаря
            return dict(user) if user else None

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

    def add_user(self, tgid):
        # Подключение к базе данных
        conn = sql.connect(self.conn_string)
        # Создание курсора для выполнения SQL-запросов
        cursor = conn.cursor()

        try:
            # Проверка существования пользователя с заданным tgid
            check_user_query = "SELECT 1 FROM category WHERE tgid = %s"
            cursor.execute(check_user_query, (tgid,))
            user_exists = cursor.fetchone() is not None

            if not user_exists:
                # Если пользователя нет, выполняем вставку
                insert_user_query = "INSERT INTO category(tgid) VALUES (%s)"
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
    
    