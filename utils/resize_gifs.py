from PIL import Image, ImageSequence
from pathlib import Path
from server.server_logger import setup_logger

logger = setup_logger("resize")

def resize_gifs(input_folder: str, output_subfolder: str = "icon_resized", size: tuple = (512, 240)):
    input_path = Path(input_folder)
    output_path = input_path / output_subfolder
    output_path.mkdir(parents=True, exist_ok=True)

    for gif in input_path.glob("*.gif"):
        try:
            with Image.open(gif) as im:
                # Проверка размеров всех кадров
                widths, heights = zip(*(frame.size for frame in ImageSequence.Iterator(im)))
                if len(set(widths)) > 1 or len(set(heights)) > 1:
                    logger.warning(f"GIF {gif.name} содержит кадры разного размера")

                # Обработка кадров
                frames = [frame.resize(size) for frame in ImageSequence.Iterator(im)]

                # Сохранение
                frames[0].save(
                    output_path / gif.name,
                    save_all=True,
                    append_images=frames[1:],
                    duration=im.info.get('duration', 100),
                    loop=0
                )
        except Exception as e:
            logger.error(f"Ошибка обработки {gif.name}: {str(e)}")
# Telegram рекомендует следующие стандарты для анимаций (гифок):
#
# Ширина: 320–512 пикселей.
#
# Высота: 240–320 пикселей.
#
# Соотношение сторон: 4:3 или 16:9.