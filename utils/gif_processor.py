from PIL import Image, ImageSequence, ImageDraw, ImageFont
from io import BytesIO
import requests
import logging
from config.settings import WEATHER_ICON_URL

logger = logging.getLogger(__name__)


def add_weather_to_gif(gif_path: str, output_path: str, weather_data: dict):
    """Добавляет виджет погоды к гифке с сохранением анимации."""
    try:
        # Проверка структуры данных
        if "error" in weather_data:
            raise RuntimeError(weather_data["error"])

        current = weather_data.get("current", {})
        forecast = weather_data.get("forecast", [])

        with Image.open(gif_path) as im:
            # Размеры оригинала
            orig_width, orig_height = im.size

            # Новый размер (сохраняем пропорции)
            scale_factor = 0.5
            new_width = int(orig_width * scale_factor)
            new_height = int(orig_height * scale_factor)

            # Загрузка иконок
            icons = []
            try:
                # Текущая погода
                icon_url = WEATHER_ICON_URL.format(icon=current.get("icon", ""))
                response = requests.get(icon_url)
                icons.append(Image.open(BytesIO(response.content)).resize((40, 40)))

                # Прогноз
                for item in forecast[:3]:
                    icon_url = WEATHER_ICON_URL.format(icon=item.get("icon", ""))
                    response = requests.get(icon_url)
                    icons.append(Image.open(BytesIO(response.content)).resize((40, 40)))
            except Exception as e:
                logger.error(f"Ошибка загрузки иконок: {str(e)}")
                raise RuntimeError("Ошибка загрузки иконок погоды")

            # Параметры виджета
            widget_width = 200
            canvas_width = new_width + widget_width
            canvas_height = max(new_height, 150)  # Минимальная высота виджета

            frames = []
            font = ImageFont.truetype("arial.ttf", 14)

            for frame in ImageSequence.Iterator(im):
                # Ресайз кадра
                resized_frame = frame.resize((new_width, new_height))

                # Создание холста
                canvas = Image.new("RGBA", (canvas_width, canvas_height), (255, 255, 255, 0))
                canvas.paste(resized_frame, (0, 0))

                # Рисуем виджет
                draw = ImageDraw.Draw(canvas)

                # Текущая погода
                y_position = 10
                canvas.paste(icons[0], (new_width + 10, y_position))
                draw.text((new_width + 60, y_position + 5),
                          f"{current.get('temp', 'N/A')}°C\n{current.get('description', '').capitalize()}",
                          font=font, fill=(0, 0, 0))

                # Прогноз
                y_position += 70
                draw.text((new_width + 10, y_position), "Прогноз:", font=font, fill=(0, 0, 0))
                y_position += 20

                for i, item in enumerate(forecast[:3]):
                    if i + 1 >= len(icons): break
                    canvas.paste(icons[i + 1], (new_width + 10, y_position))
                    draw.text((new_width + 60, y_position + 5),
                              f"{item.get('time', '')} | {item.get('temp', 'N/A')}°C",
                              font=font, fill=(0, 0, 0))
                    y_position += 50

                frames.append(canvas.convert("P"))

            # Сохранение с параметрами анимации
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
        logger.error(f"Ошибка обработки гифки: {str(e)}")
        raise RuntimeError("Не удалось создать гифку")
