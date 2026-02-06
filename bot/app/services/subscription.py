import aiosqlite
from aiogram import Bot
from aiogram.exceptions import TelegramForbiddenError

from app.core.config import settings


async def get_required_channels():
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT channel_id, link, title FROM channels WHERE is_required = 1"
        ) as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]


async def user_has_access(bot: Bot, user_id: int) -> tuple[bool, list[dict]]:
    channels = await get_required_channels()
    if not channels:
        return True, []

    missing = []
    for channel in channels:
        try:
            member = await bot.get_chat_member(chat_id=channel["channel_id"], user_id=user_id)
            if member.status in {"left", "kicked"}:
                missing.append(channel)
        except TelegramForbiddenError:
            missing.append(channel)
        except Exception:
            missing.append(channel)

    return len(missing) == 0, missing
