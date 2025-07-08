from aiogram import Dispatcher
from sqlalchemy.ext.asyncio import async_sessionmaker

from utils.middleware import DBSessionMiddleware
from .menu import router as menu_router
from .forms import router as forms_router


def setup(dp: Dispatcher, session_maker: async_sessionmaker) -> None:
    middleware = DBSessionMiddleware(session_maker)
    dp.message.middleware(middleware)
    dp.callback_query.middleware(middleware)
    dp.include_router(menu_router)
    dp.include_router(forms_router)
