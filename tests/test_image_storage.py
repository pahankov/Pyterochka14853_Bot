import unittest
from unittest.mock import AsyncMock, MagicMock
from aiogram.types import PhotoSize
from services.image_storage import save_photo


class TestImageStorage(unittest.IsolatedAsyncioTestCase):
    async def test_save_photo(self):
        mock_bot = MagicMock()
        mock_bot.download = AsyncMock()

        # Корректные параметры для PhotoSize
        mock_photo = PhotoSize(
            file_id="test",
            file_unique_id="unique_test",
            width=100,
            height=100
        )

        result = await save_photo(mock_bot, mock_photo, 123)
        self.assertIn("photos/123_offer.jpg", result)
        mock_bot.download.assert_awaited_once()
