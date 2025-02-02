import threading
from server.utils import log_time
from server.webhook_server import start_webhook_server, WebhookHandler
from server.webhook_monitor import monitor_webhook_requests
from server.server_logger import setup_server_logging
from server.publish_cloudpub import publish_cloudpub

if __name__ == '__main__':
    setup_server_logging()
    log_time("Запуск скрипта сервера...")

    # Публикация CloudPub
    log_time("Запуск публикации CloudPub...")
    publish_cloudpub()
    log_time("Публикация CloudPub завершена")

    # Логи при запуске мониторинга вебхуков
    log_time("Запуск потока мониторинга вебхуков...")
    thread_monitor = threading.Thread(target=monitor_webhook_requests)
    thread_monitor.start()
    log_time("Поток мониторинга вебхуков запущен")

    # Логи при запуске сервера вебхуков
    log_time("Запуск сервера вебхуков...")
    start_webhook_server(handler_class=WebhookHandler)
    log_time("Сервер вебхуков запущен")
