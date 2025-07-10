from datetime import datetime, timedelta
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def generate_time_slots(start: str = "10:00", end: str = "18:30", step: int = 30) -> InlineKeyboardMarkup:
    """Generate time slot buttons from start to end with given step."""
    buttons = []
    current = datetime.strptime(start, "%H:%M")
    end_time = datetime.strptime(end, "%H:%M")
    row = []
    while current <= end_time:
        time_str = current.strftime("%H:%M")
        row.append(
            InlineKeyboardButton(
                text=time_str,
                callback_data=f"time_{time_str.replace(':', '_')}"
            )
        )
        if len(row) == 3:
            buttons.append(row)
            row = []
        current += timedelta(minutes=step)
    if row:
        buttons.append(row)
    return InlineKeyboardMarkup(inline_keyboard=buttons)
