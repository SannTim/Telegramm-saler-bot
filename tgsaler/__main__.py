from tgsaler import updater, bot
import threading

def start_main():
    parallel_thread = threading.Thread(target=updater)
    parallel_thread.start()
    bot.infinity_polling()
    parallel_thread.join()
start_main()