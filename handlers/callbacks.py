from aiogram import Router, types
from aiogram.filters import Filter

router = Router()

class TextFilter(Filter):
    def __init__(self, text: str):
        self.text = text

    async def __call__(self, callback: types.CallbackQuery) -> bool:
        return callback.data == self.text

@router.callback_query(TextFilter("help"))
async def handle_help(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("📚 Справка: https://example.com/help")

@router.callback_query(TextFilter("contact"))
async def handle_contact(callback: types.CallbackQuery):
    await callback.answer()
    await callback.message.answer("📞 Телефон администрации: +7 (XXX) XXX-XX-XX")
