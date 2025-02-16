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

        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()
        dp.include_router(basic_commands.router)

        await bot.delete_webhook()
        await bot.set_webhook(
            url=f"{WEBHOOK_HOST}{WEBHOOK_PATH}",
            certificate=FSInputFile(SSL_CERT)
        )

        await run_server(bot, dp)

    except Exception as main_error:
        logger.critical(f"ФАТАЛЬНАЯ ОШИБКА: {main_error}")
        raise

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Остановка по Ctrl+C")
    except Exception as global_error:
        logger.critical(f"НЕОБРАБОТАННОЕ ИСКЛЮЧЕНИЕ: {global_error}")
