from aiogram import Router, F
from aiogram.types import Message, PhotoSize, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import create_tradein_request
from ..utils.storage import save_file
from ..utils.notifications import send_notifications
from cybershop_bot.config import Settings
from ..keyboards.menu import (
    to_menu_kb,
    contact_choice_kb,
    manual_contact_kb,
    cancel_kb,
    with_cancel,
)

router = Router()


class TradeInForm(StatesGroup):
    brand = State()
    model = State()
    photo1 = State()
    photo2 = State()
    contact = State()


@router.callback_query(F.data == "tradein_form")
async def start_tradein(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer("Производитель:", reply_markup=cancel_kb())
    await state.set_state(TradeInForm.brand)
    await callback.answer()


@router.message(TradeInForm.brand)
async def process_brand(message: Message, state: FSMContext) -> None:
    await state.update_data(brand=message.text)
    await message.delete()
    await message.answer("Модель:", reply_markup=cancel_kb())
    await state.set_state(TradeInForm.model)


@router.message(TradeInForm.model)
async def process_model(message: Message, state: FSMContext) -> None:
    await state.update_data(model=message.text)
    await message.delete()
    await message.answer("Фото 1 (внешний вид)", reply_markup=cancel_kb())
    await state.set_state(TradeInForm.photo1)


@router.message(TradeInForm.photo1)
async def process_photo1(message: Message, state: FSMContext) -> None:
    if not message.photo:
        await message.answer("Нужна фотография")
        return
    photo: PhotoSize = message.photo[-1]
    filename = f"{message.from_user.id}_photo1.jpg"
    downloaded = await photo.download()
    path = save_file(downloaded, filename, 'tradein')
    await state.update_data(photo1=path)
    await message.delete()
    await message.answer("Фото 2 (наклейка на дне)", reply_markup=cancel_kb())
    await state.set_state(TradeInForm.photo2)


@router.message(TradeInForm.photo2)
async def process_photo2(message: Message, state: FSMContext) -> None:
    if not message.photo:
        await message.answer("Нужна фотография")
        return
    photo: PhotoSize = message.photo[-1]
    filename = f"{message.from_user.id}_photo2.jpg"
    downloaded = await photo.download()
    path2 = save_file(downloaded, filename, 'tradein')
    await state.update_data(photo2=path2)
    await message.delete()
    await message.answer(
        "\U0001F4F1 \u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 \u0434\u043b\u044f \u0441\u0432\u044f\u0437\u0438:",
        reply_markup=with_cancel(contact_choice_kb()),
    )
    await state.set_state(TradeInForm.contact)


@router.callback_query(TradeInForm.contact, F.data == "use_username")
async def autofill_contact_tradein(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    username = callback.from_user.username
    contact = f"@{username}" if username else str(callback.from_user.id)
    await state.update_data(contact=contact)
    await callback.message.delete()
    await _finalize_tradein(callback.message, state, session, bot, settings)
    await callback.answer()


@router.callback_query(TradeInForm.contact, F.data == "enter_contact")
async def ask_manual_contact_tradein(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Телефон или Telegram для связи:",
        reply_markup=with_cancel(manual_contact_kb()),
    )
    await callback.answer()


@router.message(TradeInForm.contact)
async def finish_tradein(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    await state.update_data(contact=message.text)
    await message.delete()
    await _finalize_tradein(message, state, session, bot, settings)


async def _finalize_tradein(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    data = await state.get_data()
    req = await create_tradein_request(
        session,
        manufacturer=data["brand"],
        model=data["model"],
        photo1=data["photo1"],
        photo2=data["photo2"],
        contact=data["contact"],
    )
    text = (
        "\U0001F4BB Заявка на Trade-in:\n\n"
        f"\U0001F3F7 Производитель: {req.manufacturer}\n"
        f"\U0001F4C4 Модель: {req.model}\n"
        f"\U0001F4DE Контакт: {req.contact}\n"
        f"\U0001F194 TG ID: {message.from_user.id}"
    )
    await send_notifications(bot, text, settings, photo_path=req.photo1)
    await state.clear()
    await message.answer(
        "\u2705 Спасибо! Ваша заявка принята. Мы свяжемся с вами в течение дня.",
        reply_markup=to_menu_kb(),
    )
