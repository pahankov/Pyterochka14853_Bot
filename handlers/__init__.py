from .basic_commands import router as main_router
from .vacancy_handlers import router as vacancy_router
from .rate_handlers import router as rate_router  # Исправлено название
from .contact_handlers import router as contact_router

routers = [
    main_router,
    vacancy_router,
    rate_router,  # Исправлено
    contact_router
]

__all__ = ["routers"]  # Добавлено для явного экспорта
