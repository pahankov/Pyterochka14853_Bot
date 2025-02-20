from aiogram import Router, types
from pathlib import Path
from services.image_storage import get_current_offer
from server.server_logger import setup_logger

logger = setup_logger("recipe_handlers")
router = Router()


@router.callback_query(lambda c: c.data == "daily_offer")
async def handle_daily_offer(callback: types.CallbackQuery):
    offer_path = get_current_offer()

    if not offer_path or not Path(offer_path).exists():
        await callback.message.answer("🎁 Предложение дня пока не доступно.")
        await callback.answer()
        return

    try:
        await callback.message.answer_photo(types.FSInputFile(offer_path))
        await callback.answer()
    except Exception as e:
        logger.error(f"Ошибка отправки предложения: {str(e)}")
        await callback.message.answer("⚠️ Не удалось загрузить предложение дня")
