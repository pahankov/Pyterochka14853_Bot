from aiogram import Router, types
from aiogram.filters import Filter  # Импортируем базовый класс фильтра
from aiogram import F

router = Router()

# Создаем кастомный фильтр для обработки Text
class TextFilter(Filter):
    def __init__(self, startswith: str):
        self.startswith = startswith

    async def __call__(self, callback: types.CallbackQuery) -> bool:
        return callback.data.startswith(self.startswith)

@router.callback_query(TextFilter(startswith="rate_"))
async def process_rating(callback: types.CallbackQuery):
    rating = callback.data.split("_")[1]
    await callback.message.answer(f"Спасибо за оценку {rating}! 🌟")
    await callback.answer()

