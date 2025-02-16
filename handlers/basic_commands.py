import logging
import traceback
import asyncio
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile
from config.settings import GIF_FOLDER
from utils.gif_rotator import GifRotator
from utils.gif_processor import add_weather_widget
from services.weather import get_weather
from pathlib import Path

logger = logging.getLogger(__name__)
router = Router()
gif_rotator = GifRotator(GIF_FOLDER)


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="⭐ Рейтинг"))
    builder.add(types.KeyboardButton(text="🆘 Помощь"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)


def get_rating_keyboard():
    builder = ReplyKeyboardBuilder()
    for i in range(11):
        builder.add(types.KeyboardButton(text=str(i)))
    builder.adjust(5)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)


@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        # Получаем данные о погоде
        weather_data = get_weather()
        if "error" in weather_data:
            raise RuntimeError(weather_data["error"])

        # Обрабатываем гифку с виджетом погоды
        gif_path = gif_rotator.get_next_gif()
        output_path = "temp/with_weather.gif"
        add_weather_widget(gif_path, output_path, weather_data)

        # Отправляем гифку
        await message.answer_animation(FSInputFile(output_path))

        # Задержка для избежания Flood Control
        await asyncio.sleep(1)

        # Отправляем сообщение с клавиатурой
        await message.answer(
            f"Привет, {message.from_user.first_name}! Выберите действие:",
            reply_markup=get_main_keyboard()
        )
    except Exception as e:
        logger.error(f"Ошибка: {traceback.format_exc()}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")


# Остальные обработчики без изменений...

@router.message(lambda message: message.text == "⭐ Рейтинг")
async def rating_handler(message: types.Message):
    await message.answer("Оцените нас от 0 до 10:", reply_markup=get_rating_keyboard())

@router.message(lambda message: message.text.isdigit() and 0 <= int(message.text) <= 10)
async def process_rating(message: types.Message):
    rating = message.text
    await message.answer(f"Спасибо за оценку {rating}!", reply_markup=get_main_keyboard())

@router.message(lambda message: message.text == "🆘 Помощь")
async def help_handler(message: types.Message):
    await message.answer("Контакты поддержки: @support")

@router.message()
async def unknown_message(message: types.Message):
    await message.answer("Не понимаю ваше сообщение. Используйте кнопки.")
