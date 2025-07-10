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
from ..keyboards.menu import to_menu_kb, contact_choice_kb

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
    if username:
        await state.update_data(contact=f"@{username}")
        await callback.message.delete()
        await callback.message.answer("Когда с вами удобно связаться?")
        await state.set_state(ServiceForm.time)
    else:
        await callback.message.edit_text(
            "\u2757 \u0423 \u0432\u0430\u0441 \u043d\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d username \u0432 Telegram. \u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0432\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u043e\u043c\u0435\u0440 \u0440\u0443\u0447\u043d\u043e.",
            reply_markup=None,
        )
    await callback.answer()


@router.callback_query(ServiceForm.contact, F.data == "enter_contact")
async def ask_manual_contact(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Укажите телефон или Telegram:")
    await callback.answer()


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
