import os
from pathlib import Path
from aiogram.types import PhotoSize
# Инициализируем пустым значением
CURRENT_OFFER_PATH = ""

async def save_offer_photo(bot, photo: PhotoSize, user_id: int) -> str:
    global CURRENT_OFFER_PATH
    Path("offers").mkdir(exist_ok=True)
    CURRENT_OFFER_PATH = f"offers/{user_id}_offer.jpg"
    await bot.download(photo, destination=CURRENT_OFFER_PATH)
    return CURRENT_OFFER_PATH

def get_current_offer() -> str | None:
    if CURRENT_OFFER_PATH and Path(CURRENT_OFFER_PATH).exists():
        return CURRENT_OFFER_PATH
    return None
