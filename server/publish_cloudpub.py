import subprocess
import threading
import os
import sys
import io
import time

# Установим кодировку по умолчанию на UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Добавим путь к родительской директории
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from server.utils import log_time  # Импортирование log_time из server.utils

# Глобальная переменная webhook_url
webhook_url = None
url_lock = threading.Lock()

def clean_previous_sessions():
    try:
        command = 'C:\\clo\\clo.exe clean'
        result = subprocess.run(command, shell=True, capture_output=True, text=False)
        time.sleep(0.2)  # Микроскопический тайм-аут
        if result.returncode == 0:
            log_time("Предыдущие сессии CloudPub успешно очищены.")
        else:
            log_time(f"Ошибка при очистке предыдущих сессий CloudPub: Код возврата {result.returncode}.")
    except Exception as e:
        log_time(f"Ошибка при очистке предыдущих сессий CloudPub: {e}")

def extract_url(output):
    # Ищем строку, содержащую "http://localhost:443 -> https://"
    start = output.find("->") + 3
    end = len(output)
    return output[start:end].strip()

def publish_cloudpub():
    global webhook_url  # Указываем, что используем глобальную переменную
    log_time(f"Изначальное значение webhook_url: {webhook_url}")

    def run_command():
        global webhook_url  # Указываем, что используем глобальную переменную
        try:
            # Очищаем все опубликованные ресурсы перед запуском новой команды
            clean_previous_sessions()

            command = 'C:\\clo\\clo.exe publish http 443'
            log_time(f"Выполнение команды: {command}")
            process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding='utf-8')

            # Считываем вывод для получения URL
            stdout_result = ''

            while True:
                line = process.stdout.readline()
                if not line:
                    break
                stdout_result += line
                if "->" in line:
                    break

            url = extract_url(stdout_result.strip())
            with url_lock:
                log_time(f"Установка переменной webhook_url внутри run_command: {url}")
                webhook_url = url  # Сохраняем URL вебхука
                log_time(f"CloudPub успешно опубликован. URL вебхука внутри run_command: {webhook_url}")
            time.sleep(0.2)  # Микроскопический тайм-аут
        except FileNotFoundError as fnf_error:
            log_time(f"Ошибка при публикации CloudPub: Файл не найден - {fnf_error}")
        except Exception as e:
            log_time(f"Ошибка при публикации CloudPub: {e}")

    publish_thread = threading.Thread(target=run_command)
    publish_thread.start()
    publish_thread.join()  # Ждем завершения команды публикации
    log_time(f"Проверка переменной webhook_url после завершения run_command: {webhook_url}")
    log_time(f"Возвращаемое значение webhook_url: {webhook_url}")
    return webhook_url

# Запуск публикации CloudPub для проверки логов
if __name__ == "__main__":
    webhook_url = publish_cloudpub()
    log_time(f"Проверка переменной webhook_url после публикации: {webhook_url}")
