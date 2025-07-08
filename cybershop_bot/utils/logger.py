import logging
from pathlib import Path

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
