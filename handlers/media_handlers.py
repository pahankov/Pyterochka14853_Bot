from aiogram import Router, F
from aiogram.types import Message
from aiogram import Bot
from services.image_storage import save_offer_photo, get_current_offer

router = Router()

@router.message(F.photo & F.from_user.id == 1968660815)  # Только админ может загружать
async def handle_offer_photo(message: Message, bot: Bot):
    photo = message.photo[-1]
    path = await save_offer_photo(bot, photo, message.from_user.id)
    await message.answer(f"✅ Фото для 'Предложения дня' сохранено: {path}")
