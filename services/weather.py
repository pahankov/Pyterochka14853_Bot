import requests
import logging
from datetime import datetime
from config.settings import WEATHER_API_KEY, WEATHER_LAT, WEATHER_LON

logger = logging.getLogger(__name__)


def get_weather() -> dict:
    """Возвращает текущую погоду и прогноз."""
    try:
        # Текущая погода
        current_url = f"https://api.openweathermap.org/data/2.5/weather?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        current_response = requests.get(current_url)
        current_response.raise_for_status()
        current_data = current_response.json()

        # Прогноз
        forecast_url = f"https://api.openweathermap.org/data/2.5/forecast?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={WEATHER_API_KEY}&units=metric&lang=ru&cnt=4"
        forecast_response = requests.get(forecast_url)
        forecast_response.raise_for_status()
        forecast_data = forecast_response.json()

        return {
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

    except Exception as e:
        logger.error(f"Ошибка запроса погоды: {str(e)}", exc_info=True)
        return {"error": str(e)}
