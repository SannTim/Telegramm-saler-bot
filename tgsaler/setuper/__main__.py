"""Запуск всех функций необходимых для конфигурации основного модуля."""
from . import bd_creator, config_creator


def run_main():
    """Запуск всех функций необходимых для конфигурации основного модуля."""
    bd_creator.create_db()
    config_creator.create_config()


run_main()
