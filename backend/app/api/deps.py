from fastapi import Depends, Header, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.models import User
from app.db.session import get_session


async def get_current_user(
    session: AsyncSession = Depends(get_session),
    x_user_id: str | None = Header(default=None),
) -> User:
    if not x_user_id:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Відсутній ідентифікатор користувача")

    result = await session.execute(select(User).where(User.telegram_id == int(x_user_id)))
    user = result.scalar_one_or_none()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Користувача не знайдено")
    if user.banned:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Користувача заблоковано")
    return user
