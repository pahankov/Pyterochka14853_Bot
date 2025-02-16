import logging
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import FSInputFile
from config.settings import GIF_FOLDER
from utils.gif_rotator import GifRotator
from utils.gif_processor import add_weather_to_gif
from services.weather import get_weather

logger = logging.getLogger(__name__)
router = Router()
gif_rotator = GifRotator(GIF_FOLDER)


def get_main_keyboard():
    builder = ReplyKeyboardBuilder()
    buttons = [
        "⭐ Оцените нас",
        "📢 Вакансии",
        "🌐 Официальный сайт",
        "📞 Связь с администрацией",
        "📖 Рецепты",
        "🎁 Предложение дня",
        "🆘 Помощь"
    ]
    for text in buttons:
        builder.add(types.KeyboardButton(text=text))
    builder.adjust(2, 2, 2)
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
        user = message.from_user
        full_name = f"**{user.first_name} {user.last_name}**" if user.last_name else f"**{user.first_name}**"

        # Обработка гифки с погодой
        gif_path = gif_rotator.get_next_gif()
        output_path = "temp/with_weather.gif"
        weather_data = get_weather()
        if "error" in weather_data:
            raise RuntimeError(weather_data["error"])

        add_weather_to_gif(gif_path, output_path, weather_data)

        await message.answer_animation(
            FSInputFile(output_path),
            caption=f"🛒 Добро пожаловать, {full_name}!",
            parse_mode="Markdown"
        )
        # Исправление: текстовый разделитель вместо пробела
        await message.answer(
            text="\u2063",  # Невидимый разделитель (INVISIBLE SEPARATOR)
            reply_markup=get_main_keyboard()
        )
    except FileNotFoundError:
        logger.error("Файл гифки не найден")
        await message.answer("🚨 Ошибка: файл гифки не найден.")
    except RuntimeError as e:
        logger.error(f"Ошибка обработки: {e}")
        await message.answer("🚨 Ошибка при создании гифки.")
    except Exception:
        logger.error("Критическая ошибка", exc_info=True)
        await message.answer("🚨 Произошла внутренняя ошибка.")


@router.message(lambda message: message.text == "⭐ Оцените нас")
async def rating_handler(message: types.Message):
    await message.answer("Оцените нас от 0 до 10:", reply_markup=get_rating_keyboard())


@router.message(lambda message: message.text == "📢 Вакансии")
async def vacancies_handler(message: types.Message):
    await message.answer("Раздел в разработке 🛠️")


@router.message(lambda message: message.text == "🌐 Официальный сайт")
async def website_handler(message: types.Message):
    await message.answer("Сайт: https://www.x5.ru")


@router.message(lambda message: message.text == "📞 Связь с администрацией")
async def admin_handler(message: types.Message):
    await message.answer("Телефон: +7 (XXX) XXX-XX-XX")


@router.message(lambda message: message.text == "📖 Рецепты")
async def recipes_handler(message: types.Message):
    await message.answer("Рецепты скоро появятся! 📖")


@router.message(lambda message: message.text == "🎁 Предложение дня")
async def daily_offer_handler(message: types.Message):
    await message.answer("Специальные предложения обновляются ежедневно! 🎁")


@router.message(lambda message: message.text == "🆘 Помощь")
async def help_handler(message: types.Message):
    await message.answer("Контакты поддержки: @support")


@router.message(lambda message: message.text.isdigit() and 0 <= int(message.text) <= 10)
async def process_rating(message: types.Message):
    rating = message.text
    await message.answer(f"Спасибо за оценку {rating}!", reply_markup=get_main_keyboard())


@router.message()
async def unknown_message(message: types.Message):
    await message.answer("Не понимаю ваше сообщение. Используйте кнопки.")
