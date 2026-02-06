import hashlib
import hmac
from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.db.models import Offer, Transaction, User
from app.db.session import get_session
from app.services.referral import reward_referrer_once

router = APIRouter()


class PostbackPayload(BaseModel):
    sub1: int
    status: str
    offer_id: int
    signature: str


def verify_signature(sub1: int, status_value: str, offer_id: int, signature: str) -> None:
    payload = f"{sub1}:{status_value}:{offer_id}".encode("utf-8")
    expected = hmac.new(settings.postback_secret.encode("utf-8"), payload, hashlib.sha256).hexdigest()
    if not hmac.compare_digest(expected, signature):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Невалідний підпис")


@router.post("/postback")
async def postback(payload: PostbackPayload, session: AsyncSession = Depends(get_session)):
    verify_signature(payload.sub1, payload.status, payload.offer_id, payload.signature)

    if payload.status != "deposit":
        return {"ok": True, "message": "Статус не потребує обробки"}

    async with session.begin():
        user = await session.get(User, payload.sub1)
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")

        offer = await session.get(Offer, payload.offer_id)
        if not offer:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Офер не знайдено")

        user.balance_pro += offer.reward_pro
        user.is_deposit = True
        user.deposited_at = datetime.utcnow()

        session.add(
            Transaction(
                user_id=user.telegram_id,
                type="deposit",
                amount=offer.reward_pro,
                status="success",
                meta=f"Офер #{offer.id}",
            )
        )

        if user.referrer_id:
            await reward_referrer_once(session, user.referrer_id, user.telegram_id, 5000)

    return {"ok": True, "message": "Депозит підтверджено"}
