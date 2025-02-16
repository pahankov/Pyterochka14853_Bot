import requests
from config.settings import WEATHER_API_KEY, WEATHER_CITY, WEATHER_ICON_URL
from pathlib import Path

def get_weather() -> dict:
    """
    Возвращает данные о погоде: температуру, описание и URL иконки.
    """
    url = f"http://api.openweathermap.org/data/2.5/weather?q={WEATHER_CITY}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    try:
        response = requests.get(url)
        data = response.json()
        temp = data["main"]["temp"]
        description = data["weather"][0]["description"]
        icon = data["weather"][0]["icon"]
        icon_url = WEATHER_ICON_URL.format(icon=icon)
        return {
            "temp": temp,
            "description": description,
            "icon_url": icon_url
        }
    except Exception as e:
        return {"error": str(e)}

def download_icon(icon_url: str, save_path: str):
    """
    Скачивает иконку погоды.
    """
    try:
        response = requests.get(icon_url)
        with open(save_path, "wb") as f:
            f.write(response.content)
    except Exception as e:
        raise RuntimeError(f"Ошибка при загрузке иконки: {e}")
