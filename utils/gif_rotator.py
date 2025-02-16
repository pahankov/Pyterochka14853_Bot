from pathlib import Path
import os


class GifRotator:
    def __init__(self, gif_folder: str):
        self.gif_folder = Path(gif_folder)
        self.gif_list = self._load_gifs()
        self.current_index = 0

    def _load_gifs(self) -> list:
        if not self.gif_folder.exists():
            raise FileNotFoundError(f"Папка не найдена: {self.gif_folder}")

        gifs = [str(file) for file in self.gif_folder.glob("*.gif")]
        if not gifs:
            raise FileNotFoundError(f"Нет гифок в папке {self.gif_folder}")

        return gifs

    def get_next_gif(self) -> str:
        if not self.gif_list:
            raise ValueError("Список гифок пуст")

        gif_path = self.gif_list[self.current_index]
        self.current_index = (self.current_index + 1) % len(self.gif_list)
        return gif_path

    def reset(self):
        self.current_index = 0
