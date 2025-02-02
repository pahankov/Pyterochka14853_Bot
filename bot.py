import threading
from server.utils import log_time
from server.server_logger import setup_server_logging
from server.webhook_server import start_webhook_server, WebhookHandler
from server.webhook_monitor import monitor_webhook_requests
from server.publish_cloudpub import publish_cloudpub
from server.set_webhook import set_webhook, test_bot

def main():
    log_time("Начинаем инициализацию...")

    # Инициализация логирования
    log_time("Инициализация логирования...")
    setup_server_logging()

    # Публикация CloudPub
    log_time("Запуск публикации CloudPub...")
    publish_cloudpub()
    log_time("Публикация CloudPub завершена")

    # Запуск мониторинга вебхуков в отдельном потоке
    log_time("Запуск потока мониторинга вебхуков...")
    thread_monitor = threading.Thread(target=monitor_webhook_requests)
    thread_monitor.start()
    log_time("Поток мониторинга вебхуков запущен")

    # Запуск сервера вебхуков
    log_time("Запуск сервера вебхуков...")
    start_webhook_server(handler_class=WebhookHandler)
    log_time("Сервер вебхуков запущен")

    # Установка вебхука Telegram
    log_time("Установка вебхука Telegram...")
    set_webhook()
    log_time("Вебхук Telegram установлен")

    # Проверка соединения с ботом
    log_time("Проверка соединения с ботом...")
    if test_bot():
        log_time("Бот работает корректно")
        print("Бот работает корректно")
    else:
        log_time("Бот не работает корректно")
        print("Бот не работает корректно")

if __name__ == "__main__":
    main()
