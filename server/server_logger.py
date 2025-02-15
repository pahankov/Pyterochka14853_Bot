import logging
import sys
import os
from pathlib import Path
from logging.handlers import RotatingFileHandler
import colorlog

def setup_logger(name: str) -> logging.Logger:
    """Настройка логгера с цветным выводом и ротацией."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Создание папки для логов
    logs_dir = Path(__file__).resolve().parent.parent / "log"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Проверка прав
    if not os.access(logs_dir, os.W_OK):
        raise PermissionError(f"Нет прав на запись в {logs_dir}")

    # Цветной форматтер для консоли
    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s [%(filename)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    # Форматтер для файла
    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s [%(filename)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Ротируемый файловый обработчик
    file_handler = RotatingFileHandler(
        filename=logs_dir / "server.log",
        maxBytes=10 * 1024 * 1024,  # 10 MB
        backupCount=5,
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    # Консольный вывод
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)  # В консоль только INFO и выше

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
