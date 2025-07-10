from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_time_slots(start: str = "10:00", end: str = "18:30", step: int = 30) -> InlineKeyboardMarkup:
    """Return inline keyboard with time slots from start to end with step minutes."""
    buttons = []
    time = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    row = []
    while time <= end_time:
        time_str = time.strftime("%H:%M")
        row.append(
            InlineKeyboardButton(
                text=time_str,
                callback_data=f"time_{time_str.replace(':', '_')}"
            )
        )
        if len(row) == 3:
            buttons.append(row)
            row = []
        time += timedelta(minutes=step)
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
