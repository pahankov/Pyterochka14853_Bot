import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from config.settings import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH, SSL_CERT
from handlers import basic_commands
from server.server_logger import setup_logger
from server.webhook_server import run_server

logger = setup_logger("telegram_bot")

async def main():
    """Основная функция запуска бота."""
    try:
        logger.info("=" * 50)
        logger.info("████████ БОТ ЗАПУЩЕН ████████")

        # Инициализация бота и диспетчера
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(basic_commands.router)

        # Установка вебхука
        await bot.delete_webhook()
        await bot.set_webhook(
            url=f"{WEBHOOK_HOST}{WEBHOOK_PATH}",
            certificate=FSInputFile(SSL_CERT)
        )

        # Запуск сервера
        await run_server(bot, dp)

    except Exception as e:
        logger.critical(f"ФАТАЛЬНАЯ ОШИБКА: {str(e)}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановка по Ctrl+C")
    except Exception as e:
        logger.critical(f"НЕОБРАБОТАННОЕ ИСКЛЮЧЕНИЕ: {str(e)}")
        