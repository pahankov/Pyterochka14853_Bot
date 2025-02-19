import unittest
from unittest.mock import patch
import numpy as np
from utils.gif_processor import add_weather_to_gif


class TestGifProcessor(unittest.TestCase):
    @patch("utils.gif_processor.imageio.mimread")
    @patch("utils.gif_processor.imageio.mimsave")
    def test_add_weather_to_gif(self, mock_save, mock_read):
        # Создаем реалистичный мок кадра
        mock_frame = np.zeros((100, 100, 3), dtype=np.uint8)
        mock_read.return_value = [mock_frame]

        # Запуск
        weather_data = {"current": {"temp": 25}}
        add_weather_to_gif("input.gif", "output.gif", weather_data)

        # Проверка
        mock_save.assert_called_once()
