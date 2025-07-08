from aiogram import Router, F
from aiogram.types import Message

router = Router()


@router.message(F.text.startswith("/"))
async def unknown_command(message: Message) -> None:
    """Delete unknown commands from regular users."""
    await message.delete()

