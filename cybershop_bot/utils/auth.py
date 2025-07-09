from cybershop_bot.config import Settings


def is_admin(user_id: int, settings: Settings) -> bool:
    """Return True if the user is in the list of admins."""
    return user_id in settings.admin_ids
