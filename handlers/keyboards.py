from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import types

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

def get_vacancy_keyboard():
    builder = ReplyKeyboardBuilder()
    builder.add(types.KeyboardButton(text="🔙 Назад"))
    builder.add(types.KeyboardButton(text="ℹ️ Узнать"))
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True, one_time_keyboard=True)
