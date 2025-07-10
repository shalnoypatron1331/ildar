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
    manager_username: str
    manager_phone: str
    support_username: str


def get_settings() -> Settings:
    token = getenv('TOKEN', '')
    db_path = getenv('DB_PATH', 'cybershop.db')
    admin_ids = [int(x) for x in getenv('ADMIN_IDS', '').split(',') if x]
    manager_chat_id = int(getenv('MANAGER_CHAT_ID', '0'))
    manager_username = getenv('MANAGER_USERNAME', 'cybershop_manager')
    manager_phone = getenv('MANAGER_PHONE', '+7 (999) 123-45-67')
    support_username = getenv('SUPPORT_USERNAME', 'cybershop_support')
    return Settings(
        token=token,
        db_path=db_path,
        admin_ids=admin_ids,
        manager_chat_id=manager_chat_id,
        manager_username=manager_username,
        manager_phone=manager_phone,
        support_username=support_username,
    )
