from aiogram import Bot
from dataclasses import dataclass
from pathlib import Path

from ..config import Settings

async def send_notifications(
    bot: Bot,
    text: str,
    settings: Settings,
    photo_path: str | None = None,
) -> None:
    """Send a message or photo to manager chat and all admins."""
    if photo_path:
        with Path(photo_path).open('rb') as photo:
            await bot.send_photo(settings.manager_chat_id, photo, caption=text)
            for admin_id in settings.admin_ids:
                await bot.send_photo(admin_id, photo, caption=text)
    else:
        await bot.send_message(settings.manager_chat_id, text)
        for admin_id in settings.admin_ids:
            await bot.send_message(admin_id, text)
