import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from config.settings import BOT_TOKEN, WEBHOOK_HOST, WEBHOOK_PATH, SSL_CERT
from handlers import routers
from server.server_logger import setup_logger
from server.webhook_server import run_server

logger = setup_logger("telegram_bot")


async def main():
    try:
        bot = Bot(token=BOT_TOKEN)
        dp = Dispatcher()

        # Регистрация роутеров
        for router in routers:
            dp.include_router(router)

        # Настройка вебхука
        await bot.delete_webhook()
        await bot.set_webhook(
            url=f"{WEBHOOK_HOST}{WEBHOOK_PATH}",
            certificate=FSInputFile(SSL_CERT)
        )

        # Запуск сервера
        await run_server(bot, dp)

        # Логирование после успешного запуска
        logger.info("=" * 50)
        logger.info("████████ БОТ ЗАПУЩЕН ████████")

    except Exception as e:
        logger.critical(f"Ошибка: {str(e)}", exc_info=True)
        raise


if __name__ == "__main__":
    asyncio.run(main())
