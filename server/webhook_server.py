import ssl
from aiohttp import web
from aiogram import Bot, Dispatcher
from config.settings import SSL_CERT, SSL_KEY, WEBHOOK_PATH
from server.server_logger import setup_logger
import json
import asyncio
logger = setup_logger("webhook_server")
import traceback

async def handle_webhook(request: web.Request):
    try:
        # Логируем IP-адрес клиента
        client_ip = request.remote
        logger.info(f"Запрос от IP: {client_ip}")

        # Логируем заголовки
        headers = dict(request.headers)
        logger.debug(f"Заголовки: {json.dumps(headers, indent=2)}")

        # Логируем тело запроса
        data = await request.json()
        logger.debug(f"Тело: {json.dumps(data, indent=2)}")

        # Проверка наличия chat.id
        if "message" not in data or "chat" not in data["message"]:
            logger.error("Отсутствует chat.id в теле запроса")
            return web.Response(status=400, text="Bad Request")

        # Извлекаем chat.id
        chat_id = data["message"]["chat"]["id"]
        logger.info(f"Обработка сообщения от chat_id={chat_id}")

        # Передаем данные в диспетчер
        bot = request.app["bot"]
        dp = request.app["dp"]
        await dp.feed_webhook_update(bot, data)

        logger.info("Ответ сервера: 200 OK")
        return web.Response(text="OK")

    except json.JSONDecodeError:
        logger.error("Невалидный JSON")
        return web.Response(status=400, text="Invalid JSON")
    except Exception as e:
        logger.critical(f"Критическая ошибка: {traceback.format_exc()}")
        return web.Response(status=500, text="Internal Server Error")

async def run_server(bot: Bot, dp: Dispatcher):
    """Запуск асинхронного вебхук-сервера."""
    try:
        logger.info("====== НАЧАЛО ИНИЦИАЛИЗАЦИИ SSL ======")

        # Загрузка SSL
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(
            certfile=SSL_CERT,  # Путь к fullchain.pem
            keyfile=SSL_KEY     # Путь к pahankov.ru.key
        )
        logger.info(f"SSL-протокол: {ssl_context.protocol}")
        logger.info(f"Доступные шифры: {', '.join([cipher['name'] for cipher in ssl_context.get_ciphers()])}")

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

        # Бесконечный цикл для поддержания работы сервера
        while True:
            await asyncio.sleep(3600)  # Спим, чтобы сервер продолжал работать

    except Exception as e:
        logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА:\n{e}")
        raise