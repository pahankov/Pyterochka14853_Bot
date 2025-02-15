import logging
import traceback
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.exceptions import TelegramBadRequest

# Инициализация логгера
logger = logging.getLogger(__name__)

router = Router()

# Главное меню с кнопками
def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="⭐ Рейтинг"))
    builder.add(types.KeyboardButton(text="🆘 Помощь"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

# Обработчик команды /start
@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        await message.answer(
            "Привет! Я ваш бот. Выберите действие:",
            reply_markup=get_main_keyboard()
        )
    except TelegramBadRequest as e:
        logger.error(f"Ошибка Telegram API: {str(e)}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {traceback.format_exc()}")
        await message.answer("Произошла внутренняя ошибка. Пожалуйста, свяжитесь с поддержкой.")

# Обработчик кнопки "Рейтинг"
@router.message(lambda message: message.text == "⭐ Рейтинг")
async def rating_handler(message: types.Message):
    try:
        await message.answer("Оцените нас от 0 до 10:")
    except TelegramBadRequest as e:
        logger.error(f"Ошибка Telegram API: {str(e)}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {traceback.format_exc()}")
        await message.answer("Произошла внутренняя ошибка. Пожалуйста, свяжитесь с поддержкой.")

# Обработчик кнопки "Помощь"
@router.message(lambda message: message.text == "🆘 Помощь")
async def help_handler(message: types.Message):
    try:
        await message.answer("Контакты поддержки: @support")
    except TelegramBadRequest as e:
        logger.error(f"Ошибка Telegram API: {str(e)}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {traceback.format_exc()}")
        await message.answer("Произошла внутренняя ошибка. Пожалуйста, свяжитесь с поддержкой.")

# Обработчик числового рейтинга (0-10)
@router.message(lambda message: message.text.isdigit() and 0 <= int(message.text) <= 10)
async def process_rating(message: types.Message):
    try:
        rating = int(message.text)
        await message.answer(f"Спасибо за оценку {rating}!")
    except TelegramBadRequest as e:
        logger.error(f"Ошибка Telegram API: {str(e)}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {traceback.format_exc()}")
        await message.answer("Произошла внутренняя ошибка. Пожалуйста, свяжитесь с поддержкой.")

# Обработчик неизвестных сообщений
@router.message()
async def unknown_message(message: types.Message):
    try:
        await message.answer("Не понимаю ваше сообщение. Используйте кнопки.")
    except TelegramBadRequest as e:
        logger.error(f"Ошибка Telegram API: {str(e)}")
        await message.answer("Произошла ошибка. Пожалуйста, попробуйте позже.")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {traceback.format_exc()}")
        await message.answer("Произошла внутренняя ошибка. Пожалуйста, свяжитесь с поддержкой.")