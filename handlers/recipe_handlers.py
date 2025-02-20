from aiogram import Router, types
from pathlib import Path
from services.image_storage import get_current_offer
from server.server_logger import setup_logger

logger = setup_logger("recipe_handlers")
router = Router()


@router.callback_query(lambda c: c.data == "daily_offer")
async def handle_daily_offer(callback: types.CallbackQuery):
    offer_path = get_current_offer()

    if not offer_path:
        await callback.answer("🎁 Предложение дня пока не доступно.", show_alert=True)
        return

    try:
        await callback.message.answer_photo(types.FSInputFile(offer_path))
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка: {str(e)}")
        await callback.answer("⚠️ Ошибка загрузки предложения", show_alert=True)