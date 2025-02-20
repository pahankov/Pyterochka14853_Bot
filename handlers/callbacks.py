from aiogram import Router, types
from aiogram.filters import Filter
from aiogram.exceptions import TelegramBadRequest  # Добавлен импорт исключения
from server.server_logger import setup_logger
from handlers.keyboards import get_rating_keyboard
router = Router()
logger = setup_logger("callbacks")  # Инициализация логгера
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
    try:
        await callback.answer()  # Отвечаем сразу
        await callback.message.answer("📞 Телефон администрации: +7 (XXX) XXX-XX-XX")
    except TelegramBadRequest as e:
        if "query is too old" in str(e):
            logger.warning("Попытка ответить на устаревший колбэк: contact")
        else:
            raise



@router.callback_query(TextFilter("rate"))
async def handle_rate(callback: types.CallbackQuery):
    try:
        await callback.answer()
        await callback.message.answer(
            "Оцените наш сервис:",
            reply_markup=get_rating_keyboard()  # Используем новую клавиатуру
        )
    except TelegramBadRequest as e:
        logger.warning(f"Ошибка: {str(e)}")
