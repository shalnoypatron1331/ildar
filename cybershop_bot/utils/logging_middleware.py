from typing import Callable, Awaitable, Any
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Message, CallbackQuery

from .logger import log_user_action


class LoggingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        user = getattr(event, 'from_user', None)
        if user:
            if isinstance(event, Message):
                action = event.text or event.caption or '<non-text message>'
            elif isinstance(event, CallbackQuery):
                action = f'callback:{event.data}'
            else:
                action = type(event).__name__
            log_user_action(user.id, action, user.username)
        return await handler(event, data)
