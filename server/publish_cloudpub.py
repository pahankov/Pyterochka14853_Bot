import os
import time
import threading
from server.utils import log_time

def publish_cloudpub():
    log_time("Начинаем публикацию CloudPub...")

    try:
        # Публикация CloudPub
        log_time("Запуск команды для публикации CloudPub...")

        def run_command():
            start_time = time.time()
            command = 'C:\\clo\\clo.exe publish http 443'
            result = os.system(command)
            end_time = time.time()

            log_time(f"Команда публикации выполнена с кодом возврата: {result}")
            log_time(f"Время выполнения команды: {end_time - start_time:.2f} секунд")

            if result == 0:
                log_time("CloudPub успешно опубликован")
            else:
                log_time("Ошибка при публикации CloudPub")

        publish_thread = threading.Thread(target=run_command)
        publish_thread.start()

    except FileNotFoundError as fnf_error:
        log_time(f"Ошибка при публикации CloudPub: Файл не найден - {fnf_error}")
    except Exception as e:
        log_time(f"Ошибка при публикации CloudPub: {e}")
