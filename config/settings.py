import os
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).parent.parent
BOT_TOKEN = os.getenv("BOT_TOKEN")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
WEATHER_LAT = os.getenv("WEATHER_LAT", "45.028151")
WEATHER_LON = os.getenv("WEATHER_LON", "38.902729")
SSL_CERT = os.getenv("SSL_CERT")
SSL_KEY = os.getenv("SSL_KEY")
WEBHOOK_HOST = "https://pahankov.ru"
WEBHOOK_PATH = "/webhook"
GIF_FOLDER = "C:/PythonProect/Pyterochka14853_Bot/icon/icon_resized"
WEATHER_ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"
ADMIN_ID = 1968660815  # Ваш Telegram ID