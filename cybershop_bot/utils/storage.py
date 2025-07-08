from pathlib import Path
from aiogram.types import BufferedInputFile

MEDIA_DIR = Path(__file__).resolve().parents[1] / 'media'
TRADEIN_DIR = MEDIA_DIR / 'tradein'
FEEDBACK_DIR = MEDIA_DIR / 'feedback'

TRADEIN_DIR.mkdir(parents=True, exist_ok=True)
FEEDBACK_DIR.mkdir(parents=True, exist_ok=True)


def save_file(buffer: BufferedInputFile, filename: str, category: str) -> str:
    """Save uploaded file to media folder and return path."""
    if category == 'tradein':
        folder = TRADEIN_DIR
    else:
        folder = FEEDBACK_DIR
    path = folder / filename
    with path.open('wb') as f:
        f.write(buffer.read())
    return str(path)
