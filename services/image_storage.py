import os
from aiogram import Bot
from aiogram.types import PhotoSize

# Глобальная переменная для хранения пути к текущему предложению
CURRENT_OFFER_PATH = None

async def save_offer_photo(bot: Bot, photo: PhotoSize, user_id: int) -> str:
    """Сохраняет фото предложения дня и возвращает путь."""
    global CURRENT_OFFER_PATH
    os.makedirs("offers", exist_ok=True)
    CURRENT_OFFER_PATH = f"offers/{user_id}_offer.jpg"
    await bot.download(photo, destination=CURRENT_OFFER_PATH)
    return CURRENT_OFFER_PATH

def get_current_offer() -> str | None:
    """Возвращает путь к текущему предложению дня."""
    return CURRENT_OFFER_PATH if os.path.exists(CURRENT_OFFER_PATH) else None
