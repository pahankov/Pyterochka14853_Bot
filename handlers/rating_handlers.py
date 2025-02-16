from aiogram import Router, types
from .keyboards import get_main_keyboard

router = Router()

@router.message(lambda message: message.text.isdigit() and 0 <= int(message.text) <= 10)
async def process_rating(message: types.Message):
    rating = message.text
    await message.answer(
        f"Спасибо за оценку {rating}!",
        reply_markup=get_main_keyboard()
    )
