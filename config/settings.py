import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()  # Загружает переменные из .env

# Безопасное чтение из .env
BOT_TOKEN = os.getenv("BOT_TOKEN")
SSL_CERT = os.getenv("SSL_CERT")  # Путь из .env
SSL_KEY = os.getenv("SSL_KEY")
WEBHOOK_HOST = "https://pahankov.ru"
WEBHOOK_PATH = "/webhook"

# Проверка существования файлов (добавить в код)
if not Path(SSL_CERT).exists():
    raise FileNotFoundError(f"SSL_CERT не найден: {SSL_CERT}")
if not Path(SSL_KEY).exists():
    raise FileNotFoundError(f"SSL_KEY не найден: {SSL_KEY}")
