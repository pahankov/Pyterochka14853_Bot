# utils/gif_processor.py
import imageio
import numpy as np
from PIL import Image, ImageDraw
import logging
from PIL import Image, ImageDraw, ImageFont
logger = logging.getLogger(__name__)


def add_weather_to_gif(input_path: str, output_path: str, weather_data: dict):
    """Обрабатывает GIF, добавляя виджет погоды."""
    try:
        gif = imageio.mimread(input_path)
        if not gif:
            raise ValueError("GIF не содержит кадров")

        base_height, base_width, _ = gif[0].shape
        processed_frames = []

        for frame in gif:
            # Конвертация RGBA в RGB при необходимости
            if frame.shape[2] == 4:
                frame = frame[..., :3]  # Удаляем альфа-канал

            # Принудительное изменение размера
            resized_frame = frame[:base_height, :base_width, :]

            # Создаем подложку правильного формата (3 канала)
            padded_frame = np.zeros((base_height, base_width, 3), dtype=np.uint8)
            h, w = min(resized_frame.shape[0], base_height), min(resized_frame.shape[1], base_width)
            padded_frame[:h, :w] = resized_frame[:h, :w]

            # Добавление текста
            img = Image.fromarray(padded_frame)
            draw = ImageDraw.Draw(img)
            text = f"{weather_data['current']['temp']}°C"
            draw.text((10, 10), text, fill="white")

            processed_frames.append(np.array(img))
        print(f"Текст виджета: {text}")  # Логируем текст
        print(f"Размер кадра: {img.size}")  # Логируем размер
        draw.text((10, 10), text, fill="white")
        img.save("test_frame.png")  # Сохраняем тестовый кадр
        imageio.mimsave(output_path, processed_frames, duration=0.1)

    except Exception as e:
        logger.error(f"Ошибка обработки: {str(e)}", exc_info=True)
        raise RuntimeError("Не удалось создать гифку")



def combine_gif_and_weather(gif_path: str, weather_data: dict, output_path: str):
    """Склеивает GIF и виджет погоды в один файл."""
    try:
        # Загрузка GIF
        gif_frames = imageio.mimread(gif_path)
        if not gif_frames:
            raise ValueError("GIF не содержит кадров")

        # Создание виджета погоды
        widget_width = 320  # Ширина виджета
        widget = Image.new("RGB", (widget_width, gif_frames[0].shape[0]), "white")
        draw = ImageDraw.Draw(widget)
        text = f"{weather_data['current']['temp']}°C\n{weather_data['current']['description']}"
        draw.text((10, 10), text, fill="black", font=ImageFont.load_default(20))

        # Склейка кадров
        combined_frames = []
        for frame in gif_frames:
            gif_image = Image.fromarray(frame)
            combined = Image.new("RGB", (gif_image.width + widget_width, gif_image.height))
            combined.paste(gif_image, (0, 0))
            combined.paste(widget, (gif_image.width, 0))
            combined_frames.append(np.array(combined))

        # Сохранение
        imageio.mimsave(output_path, combined_frames, duration=0.1)
        return True

    except Exception as e:
        logger.error(f"Ошибка склейки: {str(e)}", exc_info=True)
        return False