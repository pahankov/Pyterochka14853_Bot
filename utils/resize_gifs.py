from PIL import Image, ImageSequence
from pathlib import Path


def resize_gifs(input_folder: str, output_subfolder: str = "icon_resized", size: tuple = (320, 240)):
    """
    Обрабатывает гифки и сохраняет их в подпапку icon_resized.
    """
    input_path = Path(input_folder)
    output_path = input_path / output_subfolder  # Создаем путь внутри icon
    output_path.mkdir(parents=True, exist_ok=True)  # Создаем папку, если её нет

    for gif in input_path.glob("*.gif"):
        with Image.open(gif) as im:
            frames = []
            for frame in ImageSequence.Iterator(im):
                frame = frame.resize(size)
                frames.append(frame)

            frames[0].save(
                output_path / gif.name,
                save_all=True,
                append_images=frames[1:],
                loop=0,
                duration=im.info['duration']
            )


if __name__ == "__main__":
    resize_gifs(
        input_folder="C:/PythonProect/Pyterochka14853_Bot/icon",
        size=(320, 320)
    )
# Telegram рекомендует следующие стандарты для анимаций (гифок):
#
# Ширина: 320–512 пикселей.
#
# Высота: 240–320 пикселей.
#
# Соотношение сторон: 4:3 или 16:9.