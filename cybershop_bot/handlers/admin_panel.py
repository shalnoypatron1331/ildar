from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import Command
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func, select

from ..config import Settings
from ..db.models import ServiceRequest, TradeInRequest, Feedback, User

router = Router()


# --- Helper database functions ---
async def count_service_requests(session: AsyncSession, category: str | None = None) -> int:
    stmt = select(func.count()).select_from(ServiceRequest)
    if category:
        stmt = stmt.where(ServiceRequest.category == category)
    result = await session.execute(stmt)
    return result.scalar_one() or 0


async def count_tradein_requests(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(TradeInRequest))
    return result.scalar_one() or 0


async def count_feedbacks(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(Feedback))
    return result.scalar_one() or 0


async def count_users(session: AsyncSession) -> int:
    result = await session.execute(select(func.count()).select_from(User))
    return result.scalar_one() or 0


async def get_service_request(session: AsyncSession, category: str, offset: int):
    result = await session.execute(
        select(ServiceRequest)
        .where(ServiceRequest.category == category)
        .order_by(ServiceRequest.id.desc())
        .offset(offset)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_tradein_request(session: AsyncSession, offset: int):
    result = await session.execute(
        select(TradeInRequest)
        .order_by(TradeInRequest.id.desc())
        .offset(offset)
        .limit(1)
    )
    return result.scalar_one_or_none()


async def get_feedback(session: AsyncSession, offset: int):
    result = await session.execute(
        select(Feedback).order_by(Feedback.id.desc()).offset(offset).limit(1)
    )
    return result.scalar_one_or_none()


# --- Keyboards ---
def admin_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="\U0001F4E5 Заявки", callback_data="admin_requests"),
                InlineKeyboardButton(text="\U0001F5C2 Отзывы", callback_data="admin_feedback"),
            ],
            [InlineKeyboardButton(text="\U0001F4CA Статистика", callback_data="admin_stats")],
        ]
    )


def requests_categories_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="\U0001F527 \u0422\u041E", callback_data="cat_maintenance"),
                InlineKeyboardButton(text="\u2699\ufe0f \u0410\u043f\u0433\u0440\u0435\u0439\u0434", callback_data="cat_upgrade"),
                InlineKeyboardButton(text="\U0001F4BB Trade-in", callback_data="cat_tradein"),
            ]
        ]
    )


def next_item_kb(prefix: str, offset: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="\U0001F4C4 \u0421\u043b\u0435\u0434\u0443\u044e\u0449\u0430\u044f", callback_data=f"{prefix}:{offset}")]
        ]
    )


@router.message(Command("admin"))
async def admin_menu(message: Message, settings: Settings) -> None:
    if message.from_user.id not in settings.admin_ids:
        await message.delete()
        return
    await message.answer("\U0001F6E0 \u041f\u0430\u043d\u0435\u043b\u044c \u0430\u0434\u043c\u0438\u043d\u0438\u0441\u0442\u0440\u0430\u0442\u043e\u0440\u0430:", reply_markup=admin_main_kb())


@router.callback_query(F.data == "admin_requests")
async def requests_summary(callback: CallbackQuery, session: AsyncSession) -> None:
    to_count = await count_service_requests(session, "maintenance")
    up_count = await count_service_requests(session, "upgrade")
    tr_count = await count_tradein_requests(session)
    total = to_count + up_count + tr_count
    text = (
        f"\U0001F4E6 \u0412\u0441\u0435\u0433\u043e \u0437\u0430\u044f\u0432\u043e\u043a: {total}\n"
        f"\U0001F527 \u0422\u041E: {to_count}\n"
        f"\u2699\ufe0f \u0410\u043f\u0433\u0440\u0435\u0439\u0434: {up_count}\n"
        f"\U0001F4BB Trade-in: {tr_count}"
    )
    await callback.message.edit_text(text, reply_markup=requests_categories_kb())
    await callback.answer()


@router.callback_query(F.data.in_({"cat_maintenance", "cat_upgrade", "cat_tradein"}))
async def show_request(callback: CallbackQuery, session: AsyncSession) -> None:
    data = callback.data
    offset = 0
    if data == "cat_maintenance":
        item = await get_service_request(session, "maintenance", offset)
        prefix = "next_maintenance"
    elif data == "cat_upgrade":
        item = await get_service_request(session, "upgrade", offset)
        prefix = "next_upgrade"
    else:
        item = await get_tradein_request(session, offset)
        prefix = "next_tradein"

    if not item:
        await callback.answer("\u041d\u0435\u0442 \u0437\u0430\u044f\u0432\u043e\u043a", show_alert=True)
        return

    if data == "cat_tradein":
        text = (
            f"#TI-{item.id}\n\n"
            f"\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c: {item.manufacturer}\n"
            f"\u041c\u043e\u0434\u0435\u043b\u044c: {item.model}\n"
            f"\u041a\u043e\u043d\u0442\u0430\u043a\u0442: {item.contact}\n"
            f"\u0414\u0430\u0442\u0430: {item.created_at.date()}"
        )
    else:
        text = (
            f"#SR-{item.id}\n\n"
            f"\u0418\u043c\u044f: {item.name}\n"
            f"\u041a\u043e\u043d\u0442\u0430\u043a\u0442: {item.phone}\n"
            f"\u0412\u0440\u0435\u043c\u044f: {item.preferred_time}\n"
            f"\u0414\u0430\u0442\u0430: {item.created_at.date()}"
        )
    await callback.message.edit_text(text, reply_markup=next_item_kb(prefix, offset + 1))
    await callback.answer()


@router.callback_query(F.data.startswith("next_"))
async def next_request(callback: CallbackQuery, session: AsyncSession) -> None:
    prefix, off = callback.data.split(":")
    offset = int(off)

    if prefix == "next_maintenance":
        item = await get_service_request(session, "maintenance", offset)
        next_prefix = prefix
    elif prefix == "next_upgrade":
        item = await get_service_request(session, "upgrade", offset)
        next_prefix = prefix
    elif prefix == "next_tradein":
        item = await get_tradein_request(session, offset)
        next_prefix = prefix
    else:
        item = await get_feedback(session, offset)
        next_prefix = prefix

    if not item:
        await callback.answer("\u0411\u043e\u043b\u044c\u0448\u0435 \u043d\u0435\u0442", show_alert=True)
        return

    if isinstance(item, TradeInRequest):
        text = (
            f"#TI-{item.id}\n\n"
            f"\u041f\u0440\u043e\u0438\u0437\u0432\u043e\u0434\u0438\u0442\u0435\u043b\u044c: {item.manufacturer}\n"
            f"\u041c\u043e\u0434\u0435\u043b\u044c: {item.model}\n"
            f"\u041a\u043e\u043d\u0442\u0430\u043a\u0442: {item.contact}\n"
            f"\u0414\u0430\u0442\u0430: {item.created_at.date()}"
        )
    elif isinstance(item, ServiceRequest):
        text = (
            f"#SR-{item.id}\n\n"
            f"\u0418\u043c\u044f: {item.name}\n"
            f"\u041a\u043e\u043d\u0442\u0430\u043a\u0442: {item.phone}\n"
            f"\u0412\u0440\u0435\u043c\u044f: {item.preferred_time}\n"
            f"\u0414\u0430\u0442\u0430: {item.created_at.date()}"
        )
    else:
        text = (
            f"#FB-{item.id}\n\n"
            f"\u041e\u0442\u0437\u044b\u0432 \u043e\u0442 {item.contact}\n"
            f"\u0422\u043e\u0432\u0430\u0440: {item.order_info}\n"
            f"\u0414\u0430\u0442\u0430: {item.created_at.date()}"
        )
    await callback.message.edit_text(text, reply_markup=next_item_kb(next_prefix, offset + 1))
    await callback.answer()


@router.callback_query(F.data == "admin_feedback")
async def show_first_feedback(callback: CallbackQuery, session: AsyncSession) -> None:
    fb = await get_feedback(session, 0)
    if not fb:
        await callback.answer("\u041e\u0442\u0437\u044b\u0432\u043e\u0432 \u043d\u0435\u0442", show_alert=True)
        return
    text = (
        f"#FB-{fb.id}\n\n"
        f"\u041e\u0442\u0437\u044b\u0432 \u043e\u0442 {fb.contact}\n"
        f"\u0422\u043e\u0432\u0430\u0440: {fb.order_info}\n"
        f"\u0414\u0430\u0442\u0430: {fb.created_at.date()}"
    )
    await callback.message.edit_text(text, reply_markup=next_item_kb("next_feedback", 1))
    await callback.answer()


@router.callback_query(F.data == "admin_stats")
async def show_stats(callback: CallbackQuery, session: AsyncSession) -> None:
    users = await count_users(session)
    to_count = await count_service_requests(session, "maintenance")
    up_count = await count_service_requests(session, "upgrade")
    trade_count = await count_tradein_requests(session)
    feedbacks = await count_feedbacks(session)
    text = (
        "\U0001F4CA \u0421\u0442\u0430\u0442\u0438\u0441\u0442\u0438\u043a\u0430:\n\n"
        f"\U0001F465 \u041f\u043e\u043b\u044c\u0437\u043e\u0432\u0430\u0442\u0435\u043b\u0435\u0439: {users}\n"
        f"\U0001F527 \u0422\u041e: {to_count}\n"
        f"\u2699\ufe0f \u0410\u043f\u0433\u0440\u0435\u0439\u0434: {up_count}\n"
        f"\U0001F4BB Trade-in: {trade_count}\n"
        f"\U0001F381 \u041e\u0442\u0437\u044b\u0432\u043e\u0432: {feedbacks}"
    )
    refresh_kb = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\u21bb \u041e\u0431\u043d\u043e\u0432\u0438\u0442\u044c", callback_data="admin_stats")]]
    )
    await callback.message.edit_text(text, reply_markup=refresh_kb)
    await callback.answer()
