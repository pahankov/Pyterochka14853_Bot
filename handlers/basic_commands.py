import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.types import FSInputFile
from pathlib import Path
import asyncio
from config.settings import GIF_FOLDER
from utils.gif_rotator import GifRotator
from utils.gif_processor import add_weather_to_gif
from services.weather import get_weather
from .keyboards import get_main_keyboard, get_rating_keyboard, get_vacancy_keyboard

logger = logging.getLogger(__name__)
router = Router()
gif_rotator = GifRotator(GIF_FOLDER)


@router.message(Command("start"))
async def start_handler(message: types.Message):
    try:
        Path("temp").mkdir(exist_ok=True)
        user = message.from_user
        full_name = f"{user.first_name} {user.last_name}" if user.last_name else user.first_name

        gif_path = gif_rotator.get_next_gif()
        output_path = "temp/weather.gif"
        weather_data = get_weather()

        if "error" in weather_data:
            raise RuntimeError(weather_data["error"])

        add_weather_to_gif(gif_path, output_path, weather_data)

        await message.answer_animation(FSInputFile(output_path))
        await asyncio.sleep(1)

        await message.answer(
            text=f"**Добро пожаловать, {full_name}!** 🛒\nВыберите действие:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )

    except FileNotFoundError as e:
        logger.error(f"FileNotFoundError: {str(e)}", exc_info=True)
        await message.answer("🚨 Файл гифки не найден.")
    except RuntimeError as e:
        logger.error(f"RuntimeError: {str(e)}", exc_info=True)
        await message.answer("🚨 Ошибка при обработке данных.")
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        await message.answer("🚨 Критическая ошибка.")


@router.message(lambda message: message.text == "⭐ Оцените нас")
async def rating_handler(message: types.Message):
    await message.answer(
        "Оцените нас от 0 до 10:",
        reply_markup=get_rating_keyboard()
    )


@router.message(lambda message: message.text == "📢 Вакансии")
async def vacancies_handler(message: types.Message):
    await message.answer(
        "На данный момент в нашем магазине вакансий нет, "
        "но вы можете узнать про вакансии в других магазинах.",
        reply_markup=get_vacancy_keyboard()
    )


@router.message(lambda message: message.text == "🌐 Официальный сайт")
async def website_handler(message: types.Message):
    await message.answer("Сайт: https://www.x5.ru")


@router.message(lambda message: message.text == "📞 Связь с администрацией")
async def admin_handler(message: types.Message):
    await message.answer("Телефон: +7 (XXX) XXX-XX-XX")


@router.message(lambda message: message.text == "📖 Рецепты")
async def recipes_handler(message: types.Message):
    await message.answer(
        "🍴 **Топ рецептов недели:**\n"
        "1. Салат 'Цезарь'\n"
        "2. Паста Карбонара\n"
        "3. Тирамису",
        parse_mode="Markdown"
    )


@router.message(lambda message: message.text == "🎁 Предложение дня")
async def daily_offer_handler(message: types.Message):
    try:
        await message.answer_photo(
            photo="https://example.com/daily_offer.jpg",
            caption="🔥 **Предложение дня!** Скидка 30% на выпечку!",
            parse_mode="Markdown"
        )
    except Exception as e:
        logger.error(f"Ошибка загрузки фото: {str(e)}", exc_info=True)
        await message.answer("🚨 Предложение дня недоступно.")


@router.message(lambda message: message.text == "🆘 Помощь")
async def help_handler(message: types.Message):
    await message.answer("Контакты поддержки: @support")


@router.message()
async def unknown_message(message: types.Message):
    await message.answer("Не понимаю ваше сообщение. Используйте кнопки.")