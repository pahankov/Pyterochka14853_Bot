import logging
from telegram import Update
from telegram.ext import CallbackContext

# Импортируем функцию настройки логирования из logger.py
from helpers.logger import setup_logging

logger = setup_logging()

class CommandHandlers:
    @staticmethod
    async def start(update: Update, context: CallbackContext) -> None:
        user = update.effective_user
        logger.info(f"Executing start command for user {user.id}")
        await update.message.reply_html(
            rf"Привет, {user.mention_html()}! Я бот Pyterochka14853. Вот список доступных команд:\n"
            "/start - Приветственное сообщение\n"
            "/help - Список доступных команд\n"
            "/ask - Задать вопрос\n"
            "/rate - Поставить оценку\n"
            "/feedback - Оставить пожелания\n"
            "/info - Получить информацию о магазине\n"
            "/jobs - Узнать о вакансиях\n"
            "/offers - Узнать о предложениях дня\n"
            "/contact - Получить контактные данные\n"
        )

    @staticmethod
    async def help_command(update: Update, context: CallbackContext) -> None:
        logger.info("Executing help command")
        await update.message.reply_text("Список доступных команд:\n/start\n/help\n/ask\n/rate\n/feedback\n/info\n/jobs\n/offers\n/contact")

    @staticmethod
    async def ask(update: Update, context: CallbackContext) -> None:
        logger.info("Executing ask command")
        await update.message.reply_text("Задайте ваш вопрос, и я постараюсь помочь!")

    @staticmethod
    async def rate(update: Update, context: CallbackContext) -> None:
        logger.info("Executing rate command")
        await update.message.reply_text("Пожалуйста, оцените наш бот от 1 до 5 звёзд!")

    @staticmethod
    async def button(update: Update, context: CallbackContext) -> None:
        logger.info("Executing button callback query")
        query = update.callback_query
        await query.answer()
        await query.edit_message_text(text=f"Вы нажали кнопку: {query.data}")

    @staticmethod
    async def feedback(update: Update, context: CallbackContext) -> None:
        logger.info("Executing feedback command")
        await update.message.reply_text("Оставьте ваши пожелания и комментарии, и мы учтём их для улучшения нашего сервиса!")

    @staticmethod
    async def info(update: Update, context: CallbackContext) -> None:
        logger.info("Executing info command")
        await update.message.reply_text("Информация о нашем магазине: Мы предлагаем широкий ассортимент товаров по доступным ценам. Подробности на нашем сайте.")

    @staticmethod
    async def jobs(update: Update, context: CallbackContext) -> None:
        logger.info("Executing jobs command")
        await update.message.reply_text("Узнайте о вакансиях в нашем магазине. Подробности на нашем сайте.")

    @staticmethod
    async def offers(update: Update, context: CallbackContext) -> None:
        logger.info("Executing offers command")
        await update.message.reply_text("Узнайте о наших предложениях дня и специальных акциях. Подробности на нашем сайте.")

    @staticmethod
    async def contact(update: Update, context: CallbackContext) -> None:
        logger.info("Executing contact command")
        await update.message.reply_text("Свяжитесь с нами: телефон +7 (800) 555-35-35, электронная почта info@pyterochka.ru")

    # Добавьте остальные команды по аналогии
