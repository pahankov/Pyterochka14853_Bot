from .basic_commands import router as basic_router
from .callbacks import router as callback_router
from .vacancy_handlers import router as vacancy_router
from .rate_handlers import router as rate_router
from .contact_handlers import router as contact_router

routers = [
    basic_router,
    callback_router,
    vacancy_router,
    rate_router,
    contact_router
]

__all__ = ["routers"]
