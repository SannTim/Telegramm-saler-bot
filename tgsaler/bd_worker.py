import psycopg2 as sql
from . import functionals


class db_controller:
    def __init__(dbinfofile) -> None:
        properties = functionals.ini_to_dict(file_path=dbinfofile)

    def get_all_by_state():
        pass
