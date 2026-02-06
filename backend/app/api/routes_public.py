from datetime import datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_current_user
from app.db.models import Offer, ReferralEvent, Transaction, User
from app.db.session import get_session

router = APIRouter(prefix="/api")


class WithdrawRequest(BaseModel):
    amount: int
    wallet: str


@router.get("/me")
async def get_me(user: User = Depends(get_current_user)):
    return {
        "telegram_id": user.telegram_id,
        "username": user.username,
        "balance_pro": user.balance_pro,
        "is_deposit": user.is_deposit,
        "banned": user.banned,
    }


@router.get("/offers")
async def get_offers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Offer).where(Offer.is_active.is_(True)))
    offers = result.scalars().all()
    return [
        {
            "id": offer.id,
            "title": offer.title,
            "reward_pro": offer.reward_pro,
            "link": offer.link,
            "is_limited": offer.is_limited,
        }
        for offer in offers
    ]


@router.get("/referrals")
async def get_referrals(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    total_result = await session.execute(
        select(func.count(User.telegram_id)).where(User.referrer_id == user.telegram_id)
    )
    total = total_result.scalar_one()

    deposit_events = await session.execute(
        select(func.count(ReferralEvent.id)).where(
            ReferralEvent.referrer_id == user.telegram_id,
            ReferralEvent.event_type == "deposit",
        )
    )
    deposits = deposit_events.scalar_one()

    return {
        "total_referrals": total,
        "deposit_referrals": deposits,
        "reward_per_invite": 1000,
        "reward_per_deposit": 5000,
    }


@router.post("/game/play")
async def play_game(user: User = Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    if not user.is_deposit:
        return {"ok": False, "message": "Бонус доступний лише після депозиту"}

    user.balance_pro += 50000
    session.add(
        Transaction(
            user_id=user.telegram_id,
            type="game_bonus",
            amount=50000,
            status="success",
            meta="Бонус за гру",
        )
    )
    await session.commit()
    return {"ok": True, "message": "Бонус нараховано", "balance_pro": user.balance_pro}


@router.get("/wallet")
async def get_wallet(user: User = Depends(get_current_user)):
    usd = round(user.balance_pro / 10000, 2)
    return {"balance_pro": user.balance_pro, "balance_usd": usd}


@router.post("/withdraw")
async def withdraw_funds(
    payload: WithdrawRequest,
    user: User = Depends(get_current_user),
    session: AsyncSession = Depends(get_session),
):
    session.add(
        Transaction(
            user_id=user.telegram_id,
            type="withdraw",
            amount=payload.amount,
            status="pending",
            meta=f"Гаманець: {payload.wallet}",
            created_at=datetime.utcnow(),
        )
    )
    await session.commit()
    return {"ok": True, "message": "Заявку на виведення створено"}
