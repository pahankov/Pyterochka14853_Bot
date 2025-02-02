import time
from server.utils import log_time

def monitor_webhook_requests():
    while True:
        log_time("Проверка запросов на сервер вебхуков...")
        time.sleep(60)  # Проверка каждые 60 секунд
