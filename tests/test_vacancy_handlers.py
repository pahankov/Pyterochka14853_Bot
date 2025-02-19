# tests/test_vacancy_handlers.py
import unittest
from unittest.mock import AsyncMock
from handlers.vacancy_handlers import vacancies_handler, back_handler
from handlers.keyboards import get_main_inline_keyboard, get_vacancy_inline_keyboard
import pytest


class TestVacancyHandlers(unittest.IsolatedAsyncioTestCase):
    @pytest.mark.asyncio
    async def test_vacancies_handler(self):
        callback = AsyncMock()
        callback.data = "vacancies"

        await vacancies_handler(callback)

        callback.message.answer.assert_called_with(
            "Вакансии в других магазинах:",
            reply_markup=get_vacancy_inline_keyboard()  # Учтён reply_markup
        )

    @pytest.mark.asyncio
    async def test_back_handler(self):
        callback = AsyncMock()

        await back_handler(callback)

        callback.message.answer.assert_called_with(
            "Главное меню:",
            reply_markup=get_main_inline_keyboard()  # Учтён reply_markup
        )
