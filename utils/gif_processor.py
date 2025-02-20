import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import requests
import logging
from io import BytesIO

logger = logging.getLogger(__name__)


def combine_gif_and_weather(gif_path: str, weather_data: dict, output_path: str) -> bool:
    """Склеивает GIF с виджетом погоды (включая иконку)"""
    try:
        # Загрузка иконки
        icon_url = f"https://openweathermap.org/img/wn/{weather_data['current']['icon']}@4x.png"
        response = requests.get(icon_url)
        icon = Image.open(BytesIO(response.content)).convert("RGBA")

        # Создание виджета
        widget_width = 400
        widget = Image.new("RGBA", (widget_width, 320), (255, 255, 255, 200))
        draw = ImageDraw.Draw(widget)

        # Добавление иконки
        widget.paste(icon, (50, 20), icon)

        # Текст погоды
        font = ImageFont.truetype("arial.ttf", 24)
        text = (
                f"Температура: {weather_data['current']['temp']}°C\n"
                f"Описание: {weather_data['current']['description']}\n"
                "Прогноз на 3 часа:\n" +
                "\n".join([f"{item['time']}: {item['temp']}°C" for item in weather_data['forecast']])
        )
        draw.multiline_text((50, 180), text, fill="black", font=font, spacing=10)

        # Обработка GIF
        gif_frames = imageio.mimread(gif_path)
        combined_frames = []

        for frame in gif_frames:
            gif_image = Image.fromarray(frame).convert("RGBA")
            combined = Image.new("RGBA", (gif_image.width + widget_width, gif_image.height))
            combined.paste(gif_image, (0, 0))
            combined.paste(widget, (gif_image.width, 0), widget)
            combined_frames.append(np.array(combined.convert("RGB")))

        imageio.mimsave(output_path, combined_frames, duration=0.1)
        return True

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        return False
