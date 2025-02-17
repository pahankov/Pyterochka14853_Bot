from aiogram import Router, types

router = Router()

@router.callback_query(lambda c: c.data == "contact")
async def contact_handler(callback: types.CallbackQuery):
    await callback.message.answer("📞 Телефон администрации: +7 (XXX) XXX-XX-XX")
    await callback.answer()
