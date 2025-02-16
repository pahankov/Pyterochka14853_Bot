import os
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent
BOT_TOKEN = os.getenv("BOT_TOKEN", "7030286976:AAG5qqKZ6p0KL0x5JssORw7fB7fU762PiUk")

# Пути к SSL-сертификатам
SSL_CERT = "C:/ssl/fullchain.pem"
SSL_KEY = "C:/ssl/pahankov.ru.key"

# Настройки вебхука
WEBHOOK_HOST = "https://pahankov.ru"
WEBHOOK_PATH = "/webhook"

# Путь к папке с гифками
GIF_FOLDER = "C:/PythonProect/Pyterochka14853_Bot/icon/icon_resized"

# Настройки для погодного API
WEATHER_API_KEY = "6ad960356f57881e23db4e8064410c2f"  # Получите на openweathermap.org
WEATHER_CITY = "Krasnodar,ru"  # Пример: Пятерочка в Москве
WEATHER_ICON_URL = "http://openweathermap.org/img/wn/{icon}@2x.png"  # URL для иконок