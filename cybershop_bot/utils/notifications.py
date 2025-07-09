from aiogram import Bot
from pathlib import Path

from ..config import Settings
from .logger import logger
from typing import Optional

async def send_notifications(
    bot: Bot,
    text: str,
    settings: Settings,
    photo_path: Optional[str] = None,
) -> None:
    """Send a message or photo to manager chat and all admins."""
    targets = [settings.manager_chat_id, *settings.admin_ids]
    if photo_path:
        for chat_id in targets:
            try:
                with Path(photo_path).open("rb") as photo:
                    await bot.send_photo(chat_id, photo, caption=text)
            except Exception as e:
                logger.error(f"Failed to send photo to {chat_id}: {e}")
    else:
        for chat_id in targets:
            try:
                await bot.send_message(chat_id, text)
            except Exception as e:
                logger.error(f"Failed to send message to {chat_id}: {e}")
