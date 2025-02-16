from PIL import Image, ImageSequence
from pathlib import Path


def resize_gifs(input_folder: str, output_subfolder: str = "icon_resized", size: tuple = (512, 240)):
    input_path = Path(input_folder)
    output_path = input_path / output_subfolder
    output_path.mkdir(parents=True, exist_ok=True)

    for gif in input_path.glob("*.gif"):  # Исправлено: убрана лишняя скобка
        with Image.open(gif) as im:
            frames = []
            durations = []
            for frame in ImageSequence.Iterator(im):
                durations.append(frame.info.get('duration', 100))
                frames.append(frame.resize(size))

            frames[0].save(
                output_path / gif.name,
                save_all=True,
                append_images=frames[1:],
                duration=durations,
                loop=0,
                disposal=2
            )
# Telegram рекомендует следующие стандарты для анимаций (гифок):
#
# Ширина: 320–512 пикселей.
#
# Высота: 240–320 пикселей.
#
# Соотношение сторон: 4:3 или 16:9.