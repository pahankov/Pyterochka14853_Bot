from PIL import Image, ImageSequence, ImageDraw, ImageFont
from io import BytesIO
import requests
import logging
from config.settings import WEATHER_ICON_URL

logger = logging.getLogger(__name__)


def add_weather_to_gif(gif_path: str, output_path: str, weather_data: dict):
    """Добавляет виджет погоды к гифке."""
    try:
        if "error" in weather_data:
            raise RuntimeError(weather_data["error"])

        current = weather_data["current"]
        forecast = weather_data["forecast"]

        with Image.open(gif_path) as im:
            # Размеры гифки
            orig_width, orig_height = im.size
            new_width = orig_width // 2
            new_height = int(orig_height * (new_width / orig_width))

            # Загрузка иконок
            icons = []
            icon_url = WEATHER_ICON_URL.format(icon=current["icon"])
            response = requests.get(icon_url)
            icons.append(Image.open(BytesIO(response.content)).resize((40, 40)))

            for item in forecast:
                icon_url = WEATHER_ICON_URL.format(icon=item["icon"])
                response = requests.get(icon_url)
                icons.append(Image.open(BytesIO(response.content)).resize((40, 40)))

            # Создание холста
            widget_width = 200
            canvas_width = new_width + widget_width
            canvas_height = max(new_height, 200)

            frames = []
            font = ImageFont.truetype("arial.ttf", 14)

            for frame in ImageSequence.Iterator(im):
                resized_frame = frame.resize((new_width, new_height))
                canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
                canvas.paste(resized_frame, (0, 0))

                # Отрисовка виджета
                draw = ImageDraw.Draw(canvas)
                canvas.paste(icons[0], (new_width + 10, 10))
                draw.text((new_width + 60, 15),
                          f"{current['temp']}°C\n{current['description'].capitalize()}",
                          font=font, fill=(0, 0, 0))

                # Прогноз
                y_pos = 80
                draw.text((new_width + 10, y_pos), "Прогноз на 3 часа:", fill=(0, 0, 0))
                y_pos += 30
                for i, item in enumerate(forecast):
                    canvas.paste(icons[i + 1], (new_width + 10, y_pos))
                    draw.text((new_width + 60, y_pos + 5),
                              f"{item['time']} | {item['temp']}°C",
                              font=font, fill=(0, 0, 0))
                    y_pos += 50

                frames.append(canvas.convert("P"))

            # Сохранение гифки
            frames[0].save(
                output_path,
                save_all=True,
                append_images=frames[1:],
                duration=im.info.get('duration', 100),
                loop=0,
                optimize=True,
                disposal=2
            )

    except Exception as e:
        logger.error(f"Ошибка обработки: {str(e)}", exc_info=True)
        raise RuntimeError("Не удалось создать гифку")
