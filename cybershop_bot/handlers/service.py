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
from ..keyboards.menu import to_menu_kb, contact_choice_kb, manual_contact_kb
from ..keyboards.time import generate_time_slots

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
    await message.answer(
        "\U0001F4F1 \u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 \u0434\u043b\u044f \u0441\u0432\u044f\u0437\u0438:",
        reply_markup=contact_choice_kb(),
    )
    await state.set_state(ServiceForm.contact)


@router.callback_query(ServiceForm.contact, F.data == "use_username")
async def autofill_contact(
    callback: CallbackQuery, state: FSMContext
) -> None:
    username = callback.from_user.username
    contact = f"@{username}" if username else str(callback.from_user.id)
    await state.update_data(contact=contact)
    await callback.message.delete()
    await callback.message.answer(
        "\u23F0 \u041a\u043e\u0433\u0434\u0430 \u0432\u0430\u043c \u0443\u0434\u043e\u0431\u043d\u043e, \u0447\u0442\u043e\u0431\u044b \u043c\u044b \u0441 \u0432\u0430\u043c\u0438 \u0441\u0432\u044f\u0437\u0430\u043b\u0438\u0441\u044c?\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0443\u0434\u043e\u0431\u043d\u043e\u0435 \u0432\u0440\u0435\u043c\u044f \u043d\u0438\u0436\u0435:",
        reply_markup=generate_time_slots(),
    )
    await state.set_state(ServiceForm.time)
    await callback.answer()


@router.callback_query(ServiceForm.contact, F.data == "enter_contact")
async def ask_manual_contact(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Укажите телефон или Telegram:", reply_markup=manual_contact_kb()
    )
    await callback.answer()


@router.message(ServiceForm.contact)
async def process_contact(message: Message, state: FSMContext) -> None:
    await state.update_data(contact=message.text)
    await message.delete()
    await message.answer(
        "\u23F0 \u041a\u043e\u0433\u0434\u0430 \u0432\u0430\u043c \u0443\u0434\u043e\u0431\u043d\u043e, \u0447\u0442\u043e\u0431\u044b \u043c\u044b \u0441 \u0432\u0430\u043c\u0438 \u0441\u0432\u044f\u0437\u0430\u043b\u0438\u0441\u044c?\n\n\u0412\u044b\u0431\u0435\u0440\u0438\u0442\u0435 \u0443\u0434\u043e\u0431\u043d\u043e\u0435 \u0432\u0440\u0435\u043c\u044f \u043d\u0438\u0436\u0435:",
        reply_markup=generate_time_slots(),
    )
    await state.set_state(ServiceForm.time)


@router.callback_query(ServiceForm.time, F.data.startswith("time_"))
async def process_time(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    time_raw = callback.data.split("_", 1)[1].replace("_", ":")
    await state.update_data(time=time_raw)
    await callback.message.delete()
    await finish_service(callback.message, state, session, bot, settings)
    await callback.answer()


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
