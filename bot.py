import sys
import io
import os
import threading
import time
import logging

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

# Установим кодировку по умолчанию на UTF-8, если не настроено
if not sys.stdout.encoding:
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
if not sys.stderr.encoding:
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8')

# Добавим путь к родительской директории и папке config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config')))
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'helpers')))

from server.utils import log_time  # Импортирование log_time из server.utils
from server.server_logger import setup_server_logging
from server.webhook_server import start_webhook_server, WebhookHandler
from server.webhook_monitor import monitor_webhook_requests
from server.publish_cloudpub import publish_cloudpub, url_lock
from server.set_webhook import set_webhook, test_bot
from config.config import TOKEN  # Импортируем токен из файла config
from helpers.buttons import ButtonHelper  # Импортируем ButtonHelper
from helpers.handlers import CommandHandlers  # Импортируем CommandHandlers

# Настройка логирования
logger = setup_server_logging()

def main():
    global webhook_url
    webhook_url = None  # Инициализируем переменную webhook_url

    log_time("Начинаем инициализацию...")

    # Инициализация логирования
    log_time("Инициализация логирования...")
    setup_server_logging()

    # Публикация CloudPub
    log_time("Запуск публикации CloudPub...")
    webhook_url = publish_cloudpub()
    log_time(f"Публикация CloudPub завершена. Полученный URL вебхука: {webhook_url}")

    # Ожидание установки URL вебхука
    while not webhook_url:
        log_time(f"Ожидание установки URL вебхука... Текущее значение: {webhook_url}")
        time.sleep(5)  # Ждем 5 секунд перед повторной проверкой

    # Проверка и логирование URL вебхука после публикации
    with url_lock:
        log_time(f"Проверка переменной webhook_url после публикации: {webhook_url}")
        if webhook_url:
            log_time(f"URL вебхука после публикации: {webhook_url}")
            # Установка вебхука Telegram с использованием webhook_url
            log_time(f"Передача переменной webhook_url в функцию set_webhook: {webhook_url}")
            set_webhook(webhook_url)
            log_time("Вебхук Telegram установлен")
        else:
            log_time("URL вебхука не установлен после публикации.")
        log_time(f"Проверка переменной webhook_url перед запуском мониторинга: {webhook_url}")

    # Запуск мониторинга вебхуков в отдельном потоке
    log_time("Запуск потока мониторинга вебхуков...")
    thread_monitor = threading.Thread(target=monitor_webhook_requests, args=(webhook_url,))
    thread_monitor.start()
    log_time("Поток мониторинга вебхуков запущен")

    # Запуск сервера вебхуков
    log_time("Запуск сервера вебхуков...")
    start_webhook_server(handler_class=WebhookHandler)
    log_time("Сервер вебхуков запущен")

    # Настройка Telegram бота
    application = ApplicationBuilder().token(TOKEN).build()

    # Регистрация обработчиков команд
    application.add_handler(CommandHandler("start", CommandHandlers.start))
    application.add_handler(CommandHandler("help", CommandHandlers.help_command))
    application.add_handler(CommandHandler("ask", CommandHandlers.ask))
    application.add_handler(CommandHandler("rate", CommandHandlers.rate))
    application.add_handler(CommandHandler("feedback", CommandHandlers.feedback))
    application.add_handler(CommandHandler("info", CommandHandlers.info))
    application.add_handler(CommandHandler("jobs", CommandHandlers.jobs))
    application.add_handler(CommandHandler("offers", CommandHandlers.offers))
    application.add_handler(CommandHandler("contact", CommandHandlers.contact))

    # Регистрация обработчика кнопок
    application.add_handler(CallbackQueryHandler(CommandHandlers.button))

    log_time("Запуск Telegram бота...")
    application.run_polling()

if __name__ == "__main__":
    main()
