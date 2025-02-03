import json
import ssl
import threading
import asyncio
from http.server import BaseHTTPRequestHandler, HTTPServer
from telegram import Update, Bot
from server.utils import log_time
from server.handlers import CommandHandlers
from config.config import TOKEN

# Инициализация глобальных переменных
bot = Bot(token=TOKEN)

def run_webhook_server(httpd):
    try:
        log_time('Сейчас запускаем сервер вебхуков с SSL...')
        httpd.serve_forever()
        log_time('Сервер вебхуков успешно запущен')
    except Exception as e:
        log_time(f"Ошибка при запуске сервера вебхуков: {e}")
    finally:
        log_time("Завершение работы сервера вебхуков")

def start_webhook_server(server_class=HTTPServer, handler_class=BaseHTTPRequestHandler, port=443):
    log_time("Начинаем настройку и запуск сервера...")
    try:
        log_time("Настройка адреса сервера и класса обработчика...")
        server_address = ('', port)
        httpd = server_class(server_address, handler_class)
        log_time("Адрес сервера и класс обработчика настроены успешно")

        log_time("Создание SSL контекста...")
        context = ssl.SSLContext(ssl.PROTOCOL_TLS)
        context.load_cert_chain(certfile="C:/PythonProect/Pyterochka14853_Bot/ssl/certificate.crt",
                                keyfile="C:/PythonProect/Pyterochka14853_Bot/ssl/private.key")
        log_time("SSL контекст создан успешно")

        log_time("Оборачивание сокета SSL контекстом...")
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)
        log_time("Сокет успешно обернут SSL контекстом")

        log_time('Проверка перед запуском сервера вебхуков с SSL...')
        log_time(f"Сервер адрес: {server_address}")
        log_time(f"SSL контекст: {context}")

        # Запуск сервера вебхуков в отдельном потоке
        log_time("Запуск потока сервера вебхуков...")
        thread = threading.Thread(target=run_webhook_server, args=(httpd,))
        thread.start()
        log_time("Поток сервера вебхуков запущен")
    except Exception as e:
        log_time(f"Ошибка при запуске: {e}")

def stop_webhook_server(httpd):
    log_time("Начинаем остановку сервера вебхуков...")
    try:
        if httpd:
            httpd.shutdown()
            httpd.server_close()
            log_time('Сервер вебхуков успешно остановлен')
    except Exception as e:
        log_time(f"Ошибка при остановке сервера: {e}")

class WebhookHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(405)
        self.end_headers()
        self.wfile.write(b"Method Not Allowed")
        log_time("GET request not allowed")

    def do_POST(self):
        try:
            log_time("Received POST request")
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            log_time(f"Received POST data: {post_data}")

            # Логирование заголовков запроса
            headers = {key: value for key, value in self.headers.items()}
            log_time(f"Request Headers: {headers}")

            update = Update.de_json(json.loads(post_data), bot)

            if update.message:
                chat_id = update.message.chat.id
                message = update.message.text
                log_time(f"Received message: {message} from chat_id: {chat_id}")

                # Обработка команд асинхронно
                asyncio.run(self.handle_message(update, message))
                log_time("Handled message successfully")

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"Webhook received")
            log_time("Processed POST request successfully")
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(b"Server error")
            log_time(f"Error in do_POST: {e}")

    @staticmethod
    async def handle_message(update: Update, message: str):
        try:
            log_time(f"Handling message: {message}")
            if message == '/start':
                await CommandHandlers.start(update, None)
            elif message == '/help':
                await CommandHandlers.help_command(update, None)
            log_time("Handled command successfully")
        except Exception as e:
            log_time(f"Error in handle_message: {e}")
