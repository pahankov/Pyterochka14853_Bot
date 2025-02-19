import unittest
from unittest.mock import AsyncMock, MagicMock, patch
from handlers.basic_commands import start_handler


class TestHandlers(unittest.IsolatedAsyncioTestCase):
    @patch("handlers.basic_commands.gif_rotator.get_next_gif")
    @patch("handlers.basic_commands.add_weather_to_gif")
    @patch("handlers.basic_commands.get_weather")
    async def test_start_handler_success(self, mock_weather, mock_add_weather, mock_get_gif):
        # Настройка моков
        mock_get_gif.return_value = "dummy.gif"
        mock_weather.return_value = {"current": {"temp": 25}}
        mock_add_weather.return_value = None

        # Вызов обработчика
        message = AsyncMock()
        message.from_user = MagicMock(first_name="Test", last_name=None)

        await start_handler(message)

        # Проверка вызовов
        message.answer_animation.assert_awaited()
        message.answer.assert_awaited()
