import imageio
import numpy as np
from PIL import Image, ImageDraw, ImageFont
import logging
from pathlib import Path

logger = logging.getLogger(__name__)


def combine_gif_and_weather(gif_path: str, weather_data: dict, output_path: str) -> bool:
    """Склеивает GIF и виджет погоды."""
    try:
        # Загрузка GIF
        gif_frames = imageio.mimread(gif_path)
        if not gif_frames:
            raise ValueError("GIF не содержит кадров")

        # Размеры
        gif_width = gif_frames[0].shape[1]
        gif_height = gif_frames[0].shape[0]
        widget_width = 300

        # Виджет погоды
        widget = Image.new("RGB", (widget_width, gif_height), "#f0f0f0")
        draw = ImageDraw.Draw(widget)

        # Шрифт (используйте свой путь при необходимости)
        try:
            font = ImageFont.truetype("arial.ttf", 28)
        except IOError:
            font = ImageFont.load_default(28)

        # Текст
        text = (
            f"🌡️ Сейчас: {weather_data['current']['temp']}°C\n"
            f"🌤️ {weather_data['current']['description'].capitalize()}\n\n"
            "🕒 Прогноз:\n"
            f"➡️ {weather_data['forecast'][0]['time']}: {weather_data['forecast'][0]['temp']}°C\n"
            f"➡️ {weather_data['forecast'][1]['time']}: {weather_data['forecast'][1]['temp']}°C\n"
            f"➡️ {weather_data['forecast'][2]['time']}: {weather_data['forecast'][2]['temp']}°C"
        )

        # Рисуем текст
        draw.multiline_text((20, 20), text, fill="#333333", font=font, spacing=12)

        # Склейка кадров
        combined_frames = []
        for frame in gif_frames:
            if frame.shape[2] == 4:
                frame = frame[..., :3]

            gif_image = Image.fromarray(frame)
            combined = Image.new("RGB", (gif_width + widget_width, gif_height))
            combined.paste(gif_image, (0, 0))
            combined.paste(widget, (gif_width, 0))
            combined_frames.append(np.array(combined))

        # Сохранение
        imageio.mimsave(output_path, combined_frames, duration=0.1)
        return True

    except Exception as e:
        logger.error(f"Ошибка склейки: {str(e)}", exc_info=True)
        return False
