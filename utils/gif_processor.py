from PIL import Image, ImageSequence, ImageDraw, ImageFont
from io import BytesIO
import requests
import logging

logger = logging.getLogger(__name__)


def add_weather_to_gif(gif_path: str, output_path: str, weather_data: dict):
    """Склеивает гифку с виджетом погоды."""
    try:
        with Image.open(gif_path) as im:
            # Уменьшаем гифку в 2 раза
            new_width = im.width // 2
            new_height = im.height // 2
            im = im.resize((new_width, new_height))

            # Загружаем иконку
            icon_url = weather_data["icon_url"]
            icon_response = requests.get(icon_url, timeout=10)
            icon = Image.open(BytesIO(icon_response.content))
            icon = icon.resize((50, 50))

            # Создаем холст
            widget_width = 100
            canvas_width = im.width + widget_width
            canvas_height = max(im.height, 100)

            frames = []
            font = ImageFont.truetype("arial.ttf", 14)
            min_duration = 50  # Минимальная длительность кадра (50 мс)

            for frame in ImageSequence.Iterator(im):
                duration = max(frame.info.get('duration', 100), min_duration)
                canvas = Image.new("RGB", (canvas_width, canvas_height), (255, 255, 255))
                canvas.paste(frame, (0, 0))
                canvas.paste(icon, (im.width + 10, 10))

                # Текст погоды
                draw = ImageDraw.Draw(canvas)
                text = (
                    f"Погода вокруг Пятёрочки:\n"
                    f"🌡️ {weather_data['temp']}°C\n"
                    f"🌤️ {weather_data['description'].capitalize()}"
                )
                draw.text((im.width + 10, 60), text, fill=(0, 0, 0), font=font)

                frames.append((canvas, duration))

            # Сохраняем гифку
            frames[0][0].save(
                output_path,
                save_all=True,
                append_images=[frame[0] for frame in frames[1:]],
                duration=[frame[1] for frame in frames],
                loop=0,
                optimize=True
            )
    except Exception as e:
        logger.error(f"Ошибка обработки гифки: {e}")
        raise RuntimeError("Не удалось создать гифку с погодой")
