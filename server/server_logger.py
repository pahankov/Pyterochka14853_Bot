import logging
import os
from pathlib import Path
import colorlog


def setup_logger(name: str) -> logging.Logger:
    """Настройка логгера с цветным выводом и записью в файл."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    logs_dir = Path(__file__).resolve().parent.parent / "log"
    logs_dir.mkdir(parents=True, exist_ok=True)

    if not os.access(logs_dir, os.W_OK):
        raise PermissionError(f"Нет прав на запись в {logs_dir}")

    file_formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s [%(filename)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    console_formatter = colorlog.ColoredFormatter(
        "%(log_color)s%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s [%(filename)s:%(lineno)d]%(reset)s",
        datefmt="%Y-%m-%d %H:%M:%S",
        log_colors={
            'DEBUG': 'cyan',
            'INFO': 'green',
            'WARNING': 'yellow',
            'ERROR': 'red',
            'CRITICAL': 'red,bg_white',
        }
    )

    file_handler = logging.FileHandler(
        filename=logs_dir / "server.log",
        mode='w',  # Перезаписывать файл
        encoding='utf-8'
    )
    file_handler.setFormatter(file_formatter)
    file_handler.setLevel(logging.DEBUG)

    console_handler = colorlog.StreamHandler()
    console_handler.setFormatter(console_formatter)
    console_handler.setLevel(logging.INFO)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger
