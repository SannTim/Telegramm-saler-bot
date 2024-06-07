from __init__ import updater, bot
import threading

parallel_thread = threading.Thread(target=updater)
parallel_thread.start()
parallel_thread.join()