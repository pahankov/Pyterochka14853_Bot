import unittest
from pathlib import Path
from tempfile import TemporaryDirectory
from unittest.mock import patch
from utils.gif_rotator import GifRotator


class TestGifRotator(unittest.TestCase):
    def setUp(self):
        self.temp_dir = TemporaryDirectory()
        self.gif_folder = Path(self.temp_dir.name)
        (self.gif_folder / "test1.gif").touch()
        (self.gif_folder / "test2.gif").touch()

    def test_get_next_gif(self):
        rotator = GifRotator(str(self.gif_folder))
        first = rotator.get_next_gif()
        second = rotator.get_next_gif()
        third = rotator.get_next_gif()

        self.assertIn("test1", first)
        self.assertIn("test2", second)
        self.assertIn("test1", third)

    def test_no_gifs_found(self):
        with TemporaryDirectory() as empty_dir:
            with self.assertRaises(FileNotFoundError):
                GifRotator(empty_dir)

    def tearDown(self):
        self.temp_dir.cleanup()
