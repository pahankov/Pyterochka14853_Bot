import unittest
from unittest.mock import patch, MagicMock
from utils.gif_processor import add_weather_to_gif
import gc  # Для явного вызова сборщика мусора
import imageio
frames = imageio.mimread("input.gif")
imageio.mimsave("output.gif", frames)
class TestGifProcessor(unittest.TestCase):
    @patch("utils.gif_processor.requests.get")
    @patch("utils.gif_processor.Image.open")
    @patch("utils.gif_processor.ImageFont.truetype")
    @patch("PIL.Image.new")  # Мок для Image.new
    @patch("PIL.ImageDraw.Draw")  # Мок для ImageDraw.Draw
    def test_add_weather_to_gif(
        self,
        mock_draw,
        mock_img_new,
        mock_font,
        mock_image_open,
        mock_get
    ):
        # 1. Мок шрифта
        mock_font.return_value = MagicMock()

        # 2. Мок изображения GIF
        mock_image = MagicMock()
        mock_image.size = (200, 200)
        mock_image.__enter__.return_value = mock_image
        mock_image.__iter__.return_value = [MagicMock()]  # Один фрейм
        mock_image.info = {"duration": 100}
        mock_image.convert.return_value = MagicMock()
        mock_image_open.return_value = mock_image

        # 3. Мок HTTP-запросов для иконок
        mock_get.return_value.content = b"fake_image"

        # 4. Мок для Image.new и ImageDraw.Draw
        mock_img_new.return_value = MagicMock()
        mock_draw.return_value = MagicMock()

        # 5. Запуск тестируемой функции
        weather_data = {
            "current": {"temp": 25, "description": "sunny", "icon": "01d"},
            "forecast": []
        }
        with patch("builtins.open", MagicMock()):
            add_weather_to_gif("input.gif", "output.gif", weather_data)

        # 6. Проверка вызовов
        mock_image.save.assert_called_once()
        mock_img_new.assert_called()
        mock_draw.assert_called()

        # 7. Явный вызов сборщика мусора
        gc.collect()

    def test_error_handling(self):
        with self.assertRaises(RuntimeError):
            add_weather_to_gif("input.gif", "output.gif", {"error": "test"})
