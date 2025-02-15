import logging  # Добавлен явный импорт
import ssl
from uuid import uuid4
from aiohttp import web
from aiogram import Bot, Dispatcher
from config.settings import SSL_CERT, SSL_KEY, WEBHOOK_PATH
from server.server_logger import setup_logger
import json
import asyncio
import traceback
from pathlib import Path

logger = setup_logger("webhook_server")


class SensitiveDataFilter(logging.Filter):
    """Фильтр для маскировки конфиденциальных данных."""

    def filter(self, record):
        if "chat_id=" in record.msg:
            record.msg = record.msg.replace("chat_id=", "chat_id=***")
        return True


logger.addFilter(SensitiveDataFilter())


async def handle_webhook(request: web.Request):
    request_id = uuid4().hex[:6]
    try:
        client_ip = request.remote
        logger.info(f"Request ID={request_id} | IP={client_ip}")

        # Логируем только ключевые заголовки
        headers = {k: v for k, v in request.headers.items() if k.lower() in {"host", "content-type"}}
        logger.debug(f"Request ID={request_id} | Headers: {json.dumps(headers, ensure_ascii=False)}")

        data = await request.json()
        logger.debug(f"Request ID={request_id} | Body: {json.dumps(data, ensure_ascii=False)}")

        if "message" not in data or "chat" not in data["message"]:
            logger.error(f"Request ID={request_id} | Отсутствует chat.id")
            return web.Response(status=400, text="Bad Request")

        chat_id = data["message"]["chat"]["id"]
        logger.info(f"Request ID={request_id} | Обработка сообщения от chat_id=***")

        bot = request.app["bot"]
        dp = request.app["dp"]
        await dp.feed_webhook_update(bot, data)

        logger.info(f"Request ID={request_id} | Ответ: 200 OK")
        return web.Response(text="OK")

    except json.JSONDecodeError:
        logger.error(f"Request ID={request_id} | Невалидный JSON")
        return web.Response(status=400, text="Invalid JSON")
    except Exception as e:
        logger.critical(f"Request ID={request_id} | Ошибка: {traceback.format_exc()}")
        return web.Response(status=500, text="Internal Server Error")


async def run_server(bot: Bot, dp: Dispatcher):
    try:
        logger.info("====== ИНИЦИАЛИЗАЦИЯ SSL ======")

        # Проверка существования сертификатов
        if not Path(SSL_CERT).exists():
            raise FileNotFoundError(f"SSL_CERT не найден: {SSL_CERT}")
        if not Path(SSL_KEY).exists():
            raise FileNotFoundError(f"SSL_KEY не найден: {SSL_KEY}")

        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(SSL_CERT, SSL_KEY)
        logger.info(f"SSL: Протокол={ssl_context.protocol} | Сертификат={SSL_CERT}")

        app = web.Application()
        app.router.add_post(WEBHOOK_PATH, handle_webhook)
        app["bot"] = bot
        app["dp"] = dp

        runner = web.AppRunner(app)
        await runner.setup()
        site = web.TCPSite(runner, "0.0.0.0", 443, ssl_context=ssl_context)
        await site.start()
        logger.info("Сервер запущен: https://0.0.0.0:443")

        while True:
            await asyncio.sleep(3600)

    except Exception as e:
        logger.critical(f"КРИТИЧЕСКАЯ ОШИБКА: {e}")
        raise
