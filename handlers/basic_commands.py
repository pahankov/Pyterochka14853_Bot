import logging
from aiogram import Router, types, F, Bot
from aiogram.filters import Command
from aiogram.types import FSInputFile
from pathlib import Path
import asyncio
from config.settings import GIF_FOLDER
from utils.gif_rotator import GifRotator
from utils.gif_processor import add_weather_to_gif
from services.weather import get_weather
from services.image_storage import save_photo
from .keyboards import get_main_inline_keyboard

logger = logging.getLogger(__name__)
router = Router()
gif_rotator = GifRotator(GIF_FOLDER)
LAST_OFFER_PHOTO: str | None = None


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
            reply_markup=get_main_inline_keyboard()
        )

    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        await message.answer("🚨 Произошла ошибка.")


@router.message(F.photo)
async def handle_photo(message: types.Message, bot: Bot):
    global LAST_OFFER_PHOTO
    try:
        file_path = await save_photo(bot, message.photo[-1], message.from_user.id)
        LAST_OFFER_PHOTO = file_path
        await message.answer("✅ Фото для «Предложения дня» сохранено!")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        await message.answer("🚨 Не удалось сохранить фото.")
