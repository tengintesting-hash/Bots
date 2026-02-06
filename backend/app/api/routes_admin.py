from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_admin_token
from app.db.models import Channel, Offer, Transaction, User
from app.db.session import get_session

router = APIRouter(prefix="/admin", dependencies=[Depends(verify_admin_token)])


class BalancePayload(BaseModel):
    amount: int


class OfferPayload(BaseModel):
    title: str
    reward_pro: int
    link: str
    is_limited: bool = False
    is_active: bool = True


class ChannelPayload(BaseModel):
    channel_id: int
    link: str
    title: str
    is_required: bool = True


@router.get("/users")
async def list_users(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(User))
    users = result.scalars().all()
    return [
        {
            "telegram_id": user.telegram_id,
            "username": user.username,
            "balance_pro": user.balance_pro,
            "is_deposit": user.is_deposit,
            "banned": user.banned,
        }
        for user in users
    ]


@router.post("/users/{user_id}/ban")
async def ban_user(user_id: int, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")
    user.banned = True
    await session.commit()
    return {"ok": True, "message": "Користувача заблоковано"}


@router.post("/users/{user_id}/balance")
async def set_balance(user_id: int, payload: BalancePayload, session: AsyncSession = Depends(get_session)):
    user = await session.get(User, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")
    user.balance_pro = payload.amount
    await session.commit()
    return {"ok": True, "message": "Баланс оновлено"}


@router.get("/offers")
async def list_offers(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Offer))
    offers = result.scalars().all()
    return [
        {
            "id": offer.id,
            "title": offer.title,
            "reward_pro": offer.reward_pro,
            "link": offer.link,
            "is_limited": offer.is_limited,
            "is_active": offer.is_active,
        }
        for offer in offers
    ]


@router.post("/offers")
async def create_offer(payload: OfferPayload, session: AsyncSession = Depends(get_session)):
    offer = Offer(**payload.model_dump())
    session.add(offer)
    await session.commit()
    await session.refresh(offer)
    return {"ok": True, "id": offer.id}


@router.put("/offers/{offer_id}")
async def update_offer(offer_id: int, payload: OfferPayload, session: AsyncSession = Depends(get_session)):
    offer = await session.get(Offer, offer_id)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Офер не знайдено")
    for field, value in payload.model_dump().items():
        setattr(offer, field, value)
    await session.commit()
    return {"ok": True, "message": "Офер оновлено"}


@router.delete("/offers/{offer_id}")
async def delete_offer(offer_id: int, session: AsyncSession = Depends(get_session)):
    offer = await session.get(Offer, offer_id)
    if not offer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Офер не знайдено")
    await session.delete(offer)
    await session.commit()
    return {"ok": True, "message": "Офер видалено"}


@router.get("/channels")
async def list_channels(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Channel))
    channels = result.scalars().all()
    return [
        {
            "channel_id": channel.channel_id,
            "link": channel.link,
            "title": channel.title,
            "is_required": channel.is_required,
        }
        for channel in channels
    ]


@router.post("/channels")
async def create_channel(payload: ChannelPayload, session: AsyncSession = Depends(get_session)):
    channel = Channel(**payload.model_dump())
    session.add(channel)
    await session.commit()
    return {"ok": True}


@router.put("/channels/{channel_id}")
async def update_channel(channel_id: int, payload: ChannelPayload, session: AsyncSession = Depends(get_session)):
    channel = await session.get(Channel, channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Канал не знайдено")
    for field, value in payload.model_dump().items():
        setattr(channel, field, value)
    await session.commit()
    return {"ok": True, "message": "Канал оновлено"}


@router.delete("/channels/{channel_id}")
async def delete_channel(channel_id: int, session: AsyncSession = Depends(get_session)):
    channel = await session.get(Channel, channel_id)
    if not channel:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Канал не знайдено")
    await session.delete(channel)
    await session.commit()
    return {"ok": True, "message": "Канал видалено"}


@router.get("/transactions")
async def list_transactions(session: AsyncSession = Depends(get_session)):
    result = await session.execute(select(Transaction))
    transactions = result.scalars().all()
    return [
        {
            "id": tx.id,
            "user_id": tx.user_id,
            "type": tx.type,
            "amount": tx.amount,
            "status": tx.status,
            "meta": tx.meta,
            "created_at": tx.created_at,
        }
        for tx in transactions
    ]
