from datetime import datetime

from sqlalchemy import Boolean, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    telegram_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    username: Mapped[str | None] = mapped_column(String(255), nullable=True)
    referrer_id: Mapped[int | None] = mapped_column(Integer, ForeignKey("users.telegram_id"), nullable=True)
    balance_pro: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    is_deposit: Mapped[bool] = mapped_column(Boolean, default=False)
    deposited_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    last_login_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    banned: Mapped[bool] = mapped_column(Boolean, default=False)

    referrer = relationship("User", remote_side=[telegram_id])


class Channel(Base):
    __tablename__ = "channels"

    channel_id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=False)
    link: Mapped[str] = mapped_column(String(255))
    title: Mapped[str] = mapped_column(String(255))
    is_required: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Offer(Base):
    __tablename__ = "offers"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255))
    reward_pro: Mapped[int] = mapped_column(Integer)
    link: Mapped[str] = mapped_column(String(255))
    is_limited: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class Transaction(Base):
    __tablename__ = "transactions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id"))
    type: Mapped[str] = mapped_column(String(50))
    amount: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(50))
    meta: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)


class ReferralEvent(Base):
    __tablename__ = "referral_events"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    referrer_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id"))
    referral_id: Mapped[int] = mapped_column(Integer, ForeignKey("users.telegram_id"))
    event_type: Mapped[str] = mapped_column(String(50))
    reward_pro: Mapped[int] = mapped_column(Integer)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
