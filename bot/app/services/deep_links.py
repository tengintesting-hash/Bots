from app.core.config import settings


def referral_link(telegram_id: int) -> str:
    return f"https://t.me/{settings.bot_username}?start=ref_{telegram_id}"
