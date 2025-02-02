import subprocess
from server.utils import log_time

webhook_set = False  # Флаг для проверки установки вебхука

def set_webhook():
    global webhook_set
    log_time("Вызов метода set_webhook")
    if not webhook_set:
        log_time("Начинаем установку вебхука Telegram... (первый вызов)")
        try:
            result_webhook = subprocess.run(
                ["curl", "-F", "url=https://unstintingly-open-nightcrawler.cloudpub.ru/webhook",
                "https://api.telegram.org/bot7030286976:AAG5qqKZ6p0KL0x5JssORw7fB7fU762PiUk/setWebhook"],
                capture_output=True, text=True)
            if result_webhook.returncode == 0:
                log_time(f"Вебхук установлен успешно: {result_webhook.stdout}")
                webhook_set = True
            else:
                log_time(f"Ошибка при установке вебхука: {result_webhook.stderr}")
        except Exception as e:
            log_time(f"Ошибка при установке вебхука: {e}")
    else:
        log_time("Вебхук уже установлен, второй вызов игнорируется")

def test_bot():
    log_time("Начинаем проверку соединения с ботом через getMe...")
    try:
        result_test = subprocess.run(
            ["curl", "https://api.telegram.org/bot7030286976:AAG5qqKZ6p0KL0x5JssORw7fB7fU762PiUk/getMe"],
            capture_output=True, text=True)
        if result_test.returncode == 0:
            log_time(f"Бот успешно прошел тест: {result_test.stdout}")
            return True
        else:
            log_time(f"Бот не прошел тест: {result_test.stderr}")
            return False
    except Exception as e:
        log_time(f"Ошибка при проверке бота: {e}")
        return False
