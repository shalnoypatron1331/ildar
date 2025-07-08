from datetime import datetime
from sqlalchemy import String, Integer, DateTime, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int] = mapped_column(primary_key=True)
    telegram_id: Mapped[int] = mapped_column(unique=True, index=True)
    username: Mapped[str | None] = mapped_column(String(32))
    first_seen: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class ServiceRequest(Base):
    __tablename__ = 'service_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int | None] = mapped_column(ForeignKey('users.id'))
    name: Mapped[str] = mapped_column(String(100))
    phone: Mapped[str] = mapped_column(String(32))
    preferred_time: Mapped[str] = mapped_column(String(100))
    category: Mapped[str] = mapped_column(String(50))  # maintenance or upgrade
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class TradeInRequest(Base):
    __tablename__ = 'tradein_requests'

    id: Mapped[int] = mapped_column(primary_key=True)
    manufacturer: Mapped[str] = mapped_column(String(100))
    model: Mapped[str] = mapped_column(String(100))
    photo1: Mapped[str]
    photo2: Mapped[str]
    contact: Mapped[str] = mapped_column(String(100))
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)

class Feedback(Base):
    __tablename__ = 'feedbacks'

    id: Mapped[int] = mapped_column(primary_key=True)
    order_info: Mapped[str] = mapped_column(String(100))
    contact: Mapped[str] = mapped_column(String(100))
    screenshot: Mapped[str]
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
