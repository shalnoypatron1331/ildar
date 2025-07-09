from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .models import User, ServiceRequest, TradeInRequest, Feedback


async def get_or_create_user(
    session: AsyncSession, telegram_id: int, username: Optional[str]
) -> User:
    result = await session.execute(select(User).where(User.telegram_id == telegram_id))
    user = result.scalar_one_or_none()
    if user:
        return user
    user = User(telegram_id=telegram_id, username=username)
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user


async def create_service_request(
    session: AsyncSession,
    user: User,
    name: str,
    contact: str,
    preferred_time: str,
    category: str,
) -> ServiceRequest:
    request = ServiceRequest(
        user_id=user.id,
        name=name,
        phone=contact,
        preferred_time=preferred_time,
        category=category,
    )
    session.add(request)
    await session.commit()
    await session.refresh(request)
    return request


async def create_tradein_request(
    session: AsyncSession,
    manufacturer: str,
    model: str,
    photo1: str,
    photo2: str,
    contact: str,
) -> TradeInRequest:
    request = TradeInRequest(
        manufacturer=manufacturer,
        model=model,
        photo1=photo1,
        photo2=photo2,
        contact=contact,
    )
    session.add(request)
    await session.commit()
    await session.refresh(request)
    return request


async def create_feedback(
    session: AsyncSession,
    order_info: str,
    contact: str,
    screenshot: str,
) -> Feedback:
    feedback = Feedback(
        order_info=order_info,
        contact=contact,
        screenshot=screenshot,
    )
    session.add(feedback)
    await session.commit()
    await session.refresh(feedback)
    return feedback
