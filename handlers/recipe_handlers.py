from aiogram import Router, types
from aiogram.types import FSInputFile
from services.image_storage import get_current_offer

router = Router()

@router.callback_query(lambda c: c.data == "daily_offer")
async def handle_daily_offer(callback: types.CallbackQuery):
    offer_path = get_current_offer()
    if offer_path:
        await callback.message.answer_photo(FSInputFile(offer_path))
    else:
        await callback.message.answer("🎁 Предложение дня пока не доступно.")
    await callback.answer()
