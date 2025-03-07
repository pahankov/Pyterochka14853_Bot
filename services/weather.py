import requests
import logging
from datetime import datetime
from config.settings import WEATHER_API_KEY, WEATHER_LAT, WEATHER_LON
from services.cache import cache

logger = logging.getLogger(__name__)
CACHE_KEY = "weather_data"


def get_weather() -> dict:
    cached = cache.get(CACHE_KEY)
    if cached:
        return cached

    try:
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        current_data = requests.get(current_url).json()

        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={WEATHER_API_KEY}&units=metric&lang=ru&cnt=4"
        forecast_data = requests.get(forecast_url).json()

        result = {
            "current": {
                "temp": current_data["main"]["temp"],
                "description": current_data["weather"][0]["description"],
                "icon": current_data["weather"][0]["icon"]
            },
            "forecast": [
                {
                    "time": datetime.fromtimestamp(item["dt"]).strftime("%H:%M"),
                    "temp": item["main"]["temp"],
                    "icon": item["weather"][0]["icon"]
                } for item in forecast_data["list"][1:4]
            ]
        }

        cache.set(CACHE_KEY, result, 1800)
        return result

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        return {"error": "Не удалось получить данные"}
