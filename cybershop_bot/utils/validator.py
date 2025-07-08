import re

PHONE_REGEX = re.compile(r'^\+?\d{10,15}$')


def is_phone_valid(phone: str) -> bool:
    return bool(PHONE_REGEX.match(phone))
