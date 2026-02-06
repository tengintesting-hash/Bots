import aiosqlite
from datetime import datetime

from app.core.config import settings


async def init_db() -> None:
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                telegram_id INTEGER PRIMARY KEY,
                username TEXT,
                referrer_id INTEGER,
                balance_pro INTEGER DEFAULT 0,
                created_at TEXT,
                is_deposit INTEGER DEFAULT 0,
                deposited_at TEXT,
                last_login_at TEXT,
                banned INTEGER DEFAULT 0
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS referral_events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                referrer_id INTEGER,
                referral_id INTEGER,
                event_type TEXT,
                reward_pro INTEGER,
                created_at TEXT
            )
            """
        )
        await db.execute(
            """
            CREATE TABLE IF NOT EXISTS channels (
                channel_id INTEGER PRIMARY KEY,
                link TEXT,
                title TEXT,
                is_required INTEGER DEFAULT 1,
                created_at TEXT
            )
            """
        )
        await db.commit()


async def get_user(telegram_id: int):
    async with aiosqlite.connect(settings.database_path) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return dict(row) if row else None


async def create_user(telegram_id: int, username: str | None, referrer_id: int | None):
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute(
            """
            INSERT OR IGNORE INTO users (telegram_id, username, referrer_id, balance_pro, created_at, last_login_at)
            VALUES (?, ?, ?, 0, ?, ?)
            """,
            (telegram_id, username, referrer_id, datetime.utcnow().isoformat(), datetime.utcnow().isoformat()),
        )
        await db.commit()


async def update_last_login(telegram_id: int):
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute(
            "UPDATE users SET last_login_at = ? WHERE telegram_id = ?",
            (datetime.utcnow().isoformat(), telegram_id),
        )
        await db.commit()


async def add_balance(telegram_id: int, amount: int):
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute(
            "UPDATE users SET balance_pro = balance_pro + ? WHERE telegram_id = ?",
            (amount, telegram_id),
        )
        await db.commit()


async def add_referral_event(referrer_id: int, referral_id: int, reward_pro: int):
    async with aiosqlite.connect(settings.database_path) as db:
        await db.execute(
            """
            INSERT INTO referral_events (referrer_id, referral_id, event_type, reward_pro, created_at)
            VALUES (?, ?, 'invite', ?, ?)
            """,
            (referrer_id, referral_id, reward_pro, datetime.utcnow().isoformat()),
        )
        await db.commit()


async def is_banned(telegram_id: int) -> bool:
    async with aiosqlite.connect(settings.database_path) as db:
        async with db.execute("SELECT banned FROM users WHERE telegram_id = ?", (telegram_id,)) as cursor:
            row = await cursor.fetchone()
            return bool(row[0]) if row else False
