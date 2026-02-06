from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import Offer


async def seed_offers(session: AsyncSession) -> None:
    result = await session.execute(select(Offer))
    offers = result.scalars().first()
    if offers:
        return

    session.add_all(
        [
            Offer(
                title="Вітаємо у PRO# Hub — бонус за реєстрацію",
                reward_pro=15000,
                link="https://example.com/bonus",
                is_limited=True,
                is_active=True,
            ),
            Offer(
                title="Щоденна місія: спробуй новий слот",
                reward_pro=8000,
                link="https://example.com/mission",
                is_limited=False,
                is_active=True,
            ),
            Offer(
                title="VIP-турнір тижня",
                reward_pro=25000,
                link="https://example.com/vip",
                is_limited=True,
                is_active=True,
            ),
        ]
    )
