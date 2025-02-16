from PIL import Image, ImageSequence, ImageDraw, ImageFont
from pathlib import Path
import requests
from io import BytesIO


def add_weather_widget(gif_path: str, output_path: str, weather_data: dict):
    """
    Добавляет виджет погоды справа от гифки.
    """
    with Image.open(gif_path) as im:
        # Создаем холст: ширина гифки + 200px под виджет
        new_width = im.width + 200
        new_height = im.height

        frames = []
        font = ImageFont.truetype("arial.ttf", 20)

        # Загружаем иконку погоды
        icon_response = requests.get(weather_data["icon_url"])
        icon = Image.open(BytesIO(icon_response.content))

        for frame in ImageSequence.Iterator(im):
            # Создаем новое изображение
            canvas = Image.new("RGBA", (new_width, new_height), (255, 255, 255))
            canvas.paste(frame, (0, 0))

            # Вставляем иконку
            canvas.paste(icon, (im.width + 10, 10), icon)

            # Рисуем текст
            draw = ImageDraw.Draw(canvas)
            draw.text(
                (im.width + 10, icon.height + 20),
                f"Погода в Пятерочке:\n{weather_data['temp']}°C\n{weather_data['description']}",
                fill=(0, 0, 0),
                font=font
            )

            frames.append(canvas)

        # Сохраняем
        frames[0].save(
            output_path,
            save_all=True,
            append_images=frames[1:],
            loop=0,
            duration=im.info['duration'],
            disposal=2
        )
        