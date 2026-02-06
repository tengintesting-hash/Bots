from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import ReferralEvent, User


async def reward_referrer_once(
    session: AsyncSession, referrer_id: int, referral_id: int, reward_pro: int
) -> bool:
    result = await session.execute(
        select(ReferralEvent).where(
            ReferralEvent.referral_id == referral_id,
            ReferralEvent.event_type == "deposit",
        )
    )
    existing = result.scalar_one_or_none()
    if existing:
        return False

    referrer = await session.get(User, referrer_id)
    if not referrer:
        return False

    referrer.balance_pro += reward_pro
    session.add(
        ReferralEvent(
            referrer_id=referrer_id,
            referral_id=referral_id,
            event_type="deposit",
            reward_pro=reward_pro,
        )
    )
    return True
