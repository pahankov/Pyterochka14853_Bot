import logging
import sys
import os
from pathlib import Path

def setup_logger(name: str) -> logging.Logger:
    """Настройка логгера с записью в файл."""
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # Создание папки для логов
    logs_dir = Path(__file__).resolve().parent.parent / "log"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Проверка прав
    if not os.access(logs_dir, os.W_OK):
        raise PermissionError(f"Нет прав на запись в {logs_dir}")

    # Форматтер
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)-15s | %(message)s [%(filename)s:%(lineno)d]",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Файловый обработчик
    file_handler = logging.FileHandler(
        filename=logs_dir / "server.log",
        mode='w',  # Перезаписывать файл
        encoding='utf-8'  # Явно указываем кодировку UTF-8
    )
    file_handler.setFormatter(formatter)

    # Консольный вывод
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger