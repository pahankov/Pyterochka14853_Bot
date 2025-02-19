import ssl
from aiohttp import web
from aiogram import Bot, Dispatcher
from config.settings import SSL_CERT, SSL_KEY, WEBHOOK_PATH
from server.server_logger import setup_logger
import asyncio

logger = setup_logger("webhook_server")

async def handle_webhook(request: web.Request):
    try:
        data = await request.json()
        logger.info(f"Получено обновление: {data}")

        # Определяем тип обновления (сообщение или колбэк)
        if "message" in data:
            chat_id = data["message"]["chat"]["id"]
            logger.info(f"Обработка сообщения от chat_id={chat_id}")
        elif "callback_query" in data:
            chat_id = data["callback_query"]["message"]["chat"]["id"]
            logger.info(f"Обработка колбэка от chat_id={chat_id}")
        else:
            logger.error("Неизвестный тип обновления")
            return web.Response(status=400)

        # Передаем данные в диспетчер
        bot = request.app["bot"]
        dp = request.app["dp"]
        await dp.feed_webhook_update(bot, data)

        return web.Response(text="OK")
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}", exc_info=True)
        return web.Response(status=500)

async def run_server(bot: Bot, dp: Dispatcher):
    """Запуск асинхронного вебхук-сервера."""
    try:
        logger.info("====== НАЧАЛО ИНИЦИАЛИЗАЦИИ SSL ======")

        # Загрузка SSL
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            certfile=SSL_CERT,
            keyfile=SSL_KEY
        )

        # Создание приложения aiohttp
        app = web.Application()
        app.router.add_post(WEBHOOK_PATH, handle_webhook)
        app["bot"] = bot
        app["dp"] = dp

        # Запуск сервера
        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 443, ssl_context=ssl_context)
        await site.start()
        logger.info("Сервер запущен на https://0.0.0.0:443")
        logger.info("=" * 50)
        logger.info("████████ БОТ ЗАПУЩЕН ████████")  # Лог здесь

        # Бесконечный цикл для поддержания работы сервера
        while True:
            await asyncio.sleep(3600)

    except Exception as e:
        logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА:\n{e}")
        raise
