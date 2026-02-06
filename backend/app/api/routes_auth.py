from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.security import verify_telegram_init_data
from app.db.models import User
from app.db.session import get_session

router = APIRouter(prefix="/api/auth")


class AuthPayload(BaseModel):
    initData: str




@router.post("/telegram")
async def auth_telegram(payload: AuthPayload, session: AsyncSession = Depends(get_session)):
    data = verify_telegram_init_data(payload.initData)
    if "user" in data:
        import json

        user_data = json.loads(data["user"])
        user_id = int(user_data.get("id"))
        username = user_data.get("username")
    else:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Відсутні дані користувача")

    result = await session.execute(select(User).where(User.telegram_id == user_id))
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_id=user_id, username=username, created_at=datetime.utcnow())
        session.add(user)
    else:
        user.username = username

    user.last_login_at = datetime.utcnow()
    await session.commit()
    await session.refresh(user)

    return {
        "telegram_id": user.telegram_id,
        "username": user.username,
        "balance_pro": user.balance_pro,
        "is_deposit": user.is_deposit,
        "banned": user.banned,
    }

