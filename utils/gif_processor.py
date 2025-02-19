import imageio
import numpy as np
from PIL import Image
import logging

logger = logging.getLogger(__name__)


def add_weather_to_gif(input_path: str, output_path: str, weather_data: dict):
    """Обрабатывает GIF, добавляя виджет погоды."""
    try:
        # Чтение GIF
        gif = imageio.mimread(input_path)
        if not gif:
            raise ValueError("GIF не содержит кадров")

        # Определение базового размера
        base_width, base_height = Image.fromarray(gif[0]).size
        processed_frames = []

        for frame in gif:
            # Конвертация в Pillow Image для изменения размера
            img = Image.fromarray(frame)
            if img.size != (base_width, base_height):
                img = img.resize((base_width, base_height))

            # Конвертация обратно в numpy array
            processed_frames.append(np.array(img))

        # Сохранение
        imageio.mimsave(output_path, processed_frames, duration=0.1)

    except Exception as e:
        logger.error(f"Ошибка обработки: {str(e)}", exc_info=True)
        raise RuntimeError("Не удалось создать гифку")
