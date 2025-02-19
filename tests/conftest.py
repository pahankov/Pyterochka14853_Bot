import sys
import os
import pytest
from aiogram import Dispatcher, Bot
from aiogram.enums import ParseMode
import asyncio
# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

@pytest.fixture
def bot():
    return Bot(token="test", parse_mode=ParseMode.HTML)

@pytest.fixture
def dp():
    return Dispatcher()

@pytest.fixture(scope="session")  # Явно указываем область видимости
def event_loop():
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()