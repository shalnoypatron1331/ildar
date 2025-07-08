import logging
from pathlib import Path
from datetime import datetime
import os

LOG_FILE = Path(__file__).resolve().parents[1] / 'logs' / 'logs.txt'
LOG_FILE.parent.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(name)s: %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
    ]
)

logger = logging.getLogger('bot')


def log_user_action(user_id: int, text: str, username: str | None = None) -> None:
    """Log a single user action to a dedicated file."""
    folder = Path(__file__).resolve().parents[1] / 'logs' / str(user_id)
    os.makedirs(folder, exist_ok=True)

    timestamp = datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    nick = f"@{username}" if username else ""
    log_line = f"{timestamp} User {nick} нажал: {text}\n"

    with open(folder / 'actions.txt', 'a', encoding='utf-8') as f:
        f.write(log_line)
