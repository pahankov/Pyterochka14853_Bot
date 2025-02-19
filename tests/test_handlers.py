# tests/test_handlers.py
import pytest
import unittest
from unittest.mock import AsyncMock, MagicMock
from aiogram import types
from handlers.basic_commands import start_handler
from handlers.rate_handlers import process_rating

class TestHandlers(unittest.IsolatedAsyncioTestCase):
    @pytest.mark.asyncio
    async def test_start_handler_success(self):
        message = AsyncMock()
        message.from_user = MagicMock(first_name="Test", last_name=None)

        await start_handler(message)

        message.answer_animation.assert_awaited()
        message.answer.assert_awaited()

    @pytest.mark.asyncio
    async def test_rate_handler(self):
        callback = AsyncMock()
        callback.data = "rate_5"

        await process_rating(callback)

        callback.message.answer.assert_called_with("Спасибо за оценку 5! 🌟")
