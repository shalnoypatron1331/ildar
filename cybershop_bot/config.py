from dataclasses import dataclass
from os import getenv
from pathlib import Path
from typing import List

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / '.env')

@dataclass
class Settings:
    token: str
    db_path: str
    admin_ids: List[int]
    manager_chat_id: int


def get_settings() -> Settings:
    token = getenv('TOKEN', '')
    db_path = getenv('DB_PATH', 'cybershop.db')
    admin_ids = [int(x) for x in getenv('ADMIN_IDS', '').split(',') if x]
    manager_chat_id = int(getenv('MANAGER_CHAT_ID', '0'))
    return Settings(
        token=token,
        db_path=db_path,
        admin_ids=admin_ids,
        manager_chat_id=manager_chat_id,
    )
