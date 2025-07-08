from aiogram import Dispatcher

from .menu import router as menu_router
from .service import router as service_router
from .tradein import router as tradein_router
from .feedback import router as feedback_router
from .admin_panel import router as admin_router
from .security import router as security_router


def register_handlers(dp: Dispatcher) -> None:
    dp.include_router(menu_router)
    dp.include_router(service_router)
    dp.include_router(tradein_router)
    dp.include_router(feedback_router)
    dp.include_router(admin_router)
    dp.include_router(security_router)
