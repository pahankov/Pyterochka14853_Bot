from aiogram import Router, types
from server.server_logger import setup_logger
router = Router()
logger = setup_logger("contact_handlers")
@router.callback_query(lambda c: c.data == "contact")
async def contact_handler(callback: types.CallbackQuery):
    logger.info("Обработчик contact_handler вызван")
    await callback.message.answer("📞 Телефон администрации: +7 (XXX) XXX-XX-XX")
    await callback.answer()
