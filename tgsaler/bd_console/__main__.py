"""Запуск cmd."""
from . import app


def run_main():
    """Запуск cmd."""
    cm = app()
    cm.cmdloop()
