import sys
import os

# Установим путь к папке config
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'config')))
from config import config

import requests
from server.utils import log_time

def set_webhook(webhook_url):
    try:
        # Логируем значение webhook_url, чтобы убедиться, что оно передается
        log_time(f"Функция set_webhook получила значение webhook_url: {webhook_url}")

        # Используем переменную webhook_url, переданную как параметр
        log_time(f"Установка вебхука на URL: {webhook_url}")
        # Логика установки вебхука
        url = f"https://api.telegram.org/bot{config.TOKEN}/setWebhook?url={webhook_url}"
        log_time(f"Запрос к Telegram API: {url}")
        response = requests.post(url)
        log_time(f"Ответ от Telegram: {response.json()}")
    except Exception as e:
        log_time(f"Ошибка при установке вебхука: {e}")

def test_bot():
    try:
        # Логика проверки соединения с ботом
        response = requests.get(f"https://api.telegram.org/bot{config.TOKEN}/getMe")
        return response.status_code == 200
    except Exception as e:
        log_time(f"Ошибка при проверке соединения с ботом: {e}")
        return False
