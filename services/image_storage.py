import os
from aiogram import Bot
from aiogram.types import PhotoSize  # Правильный импорт

async def save_photo(bot: Bot, photo: PhotoSize, user_id: int) -> str:
    """Сохраняет фото в папку photos/ и возвращает путь."""
    os.makedirs("photos", exist_ok=True)
    file_path = f"photos/{user_id}_offer.jpg"
    await bot.download(photo, destination=file_path)
    return file_path