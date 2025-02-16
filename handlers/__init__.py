from .basic_commands import router as basic_router
from .vacancy_handlers import router as vacancy_router
from .rating_handlers import router as rating_router

routers = [
    vacancy_router,
    rating_router,
    basic_router  # Обработчик unknown_message должен быть последним
]

__all__ = ["routers"]
