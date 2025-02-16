import requests
import logging
from config.settings import WEATHER_API_KEY, WEATHER_LAT, WEATHER_LON, WEATHER_ICON_URL

logger = logging.getLogger(__name__)


def get_weather() -> dict:
    """Возвращает данные о погоде."""
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={WEATHER_LAT}&lon={WEATHER_LON}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        logger.debug(f"Данные погоды: {data}")

        return {
            "temp": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "icon_url": WEATHER_ICON_URL.format(icon=data["weather"][0]["icon"]),
            "address": "📍 Пятерочка, ул. Примерная, 123"
        }
    except requests.exceptions.RequestException as e:
        logger.error(f"Ошибка запроса: {e}")
        return {"error": str(e)}
    except (KeyError, IndexError) as e:
        logger.error(f"Ошибка парсинга данных: {e}")
        return {"error": "Неверный формат данных"}
