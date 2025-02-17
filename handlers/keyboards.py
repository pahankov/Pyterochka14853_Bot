from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_main_inline_keyboard():
    builder = InlineKeyboardBuilder()
    buttons = [
        ("⭐ Оценить", "rate"),
        ("📢 Вакансии", "vacancies"),
        ("🌐 Сайт", "https://www.x5.ru"),
        ("📞 Связь", "contact"),
        ("🎁 Предложение дня", "daily_offer"),
        ("📖 Рецепты", "recipes"),
        ("🆘 Помощь", "help")
    ]
    for text, data in buttons:
        if data.startswith("http"):
            builder.button(text=text, url=data)
        else:
            builder.button(text=text, callback_data=data)
    builder.adjust(2, 2, 2, 1)
    return builder.as_markup()

def get_vacancy_inline_keyboard():  # Добавлена функция
    builder = InlineKeyboardBuilder()
    builder.button(text="🔙 Назад", callback_data="back")
    builder.button(text="ℹ️ Узнать", url="https://career.x5.ru")
    builder.adjust(2)
    return builder.as_markup()
