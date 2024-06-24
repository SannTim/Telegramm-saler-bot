"""Запускает обновление данных для бота и самого бота."""
from tgsaler import updater, bot
import threading


def start_main():
    """Запускает обновление данных для бота и самого бота."""
    parallel_thread = threading.Thread(target=updater)
    parallel_thread.start()
    bot.infinity_polling()
    parallel_thread.join()


start_main()
