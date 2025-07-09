from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import (
    get_or_create_user,
    create_service_request,
)
from ..utils.notifications import send_notifications
from cybershop_bot.config import Settings
from ..keyboards.menu import to_menu_kb

router = Router()


class ServiceForm(StatesGroup):
    name = State()
    contact = State()
    time = State()


@router.callback_query(F.data.in_({"maintenance", "upgrade"}))
async def start_service(callback: CallbackQuery, state: FSMContext) -> None:
    category = callback.data
    await state.update_data(category=category)
    await callback.message.delete()
    await callback.message.answer("Введите ваше имя:")
    await state.set_state(ServiceForm.name)
    await callback.answer()


@router.message(ServiceForm.name)
async def process_name(message: Message, state: FSMContext) -> None:
    await state.update_data(name=message.text)
    await message.delete()
    await message.answer("Укажите телефон или Telegram:")
    await state.set_state(ServiceForm.contact)


@router.message(ServiceForm.contact)
async def process_contact(message: Message, state: FSMContext) -> None:
    await state.update_data(contact=message.text)
    await message.delete()
    await message.answer("Когда с вами удобно связаться?")
    await state.set_state(ServiceForm.time)


@router.message(ServiceForm.time)
async def process_time(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    await state.update_data(time=message.text)
    await message.delete()
    await finish_service(message, state, session, bot, settings)


async def finish_service(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    data = await state.get_data()
    user = await get_or_create_user(session, message.from_user.id, message.from_user.username)
    req = await create_service_request(
        session,
        user=user,
        name=data["name"],
        contact=data["contact"],
        preferred_time=data["time"],
        category=data["category"],
    )
    text = (
        "\U0001F6E0 Новая заявка на ТО:\n\n"
        f"\U0001F464 Имя: {req.name}\n"
        f"\U0001F4DE Контакт: {req.phone}\n"
        f"\U0001F551 Время: {req.preferred_time}\n\n"
        f"\U0001F194 TG ID: {message.from_user.id}"
    )
    await send_notifications(bot, text, settings)
    await message.answer(
        "\u2705 Спасибо! Ваша заявка принята. Мы свяжемся с вами в течение дня.",
        reply_markup=to_menu_kb(),
    )
    await state.clear()
