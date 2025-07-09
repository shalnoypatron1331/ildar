from aiogram import Router, F
from aiogram.types import Message, PhotoSize, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import create_tradein_request
from ..utils.storage import save_file
from ..utils.notifications import send_notifications
from cybershop_bot.config import Settings
from ..keyboards.menu import to_menu_kb

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
    await callback.message.answer("Производитель:")
    await state.set_state(TradeInForm.brand)
    await callback.answer()


@router.message(TradeInForm.brand)
async def process_brand(message: Message, state: FSMContext) -> None:
    await state.update_data(brand=message.text)
    await message.delete()
    await message.answer("Модель:")
    await state.set_state(TradeInForm.model)


@router.message(TradeInForm.model)
async def process_model(message: Message, state: FSMContext) -> None:
    await state.update_data(model=message.text)
    await message.delete()
    await message.answer("Фото 1 (внешний вид)")
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
    await message.answer("Фото 2 (наклейка на дне)")
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
    await message.answer("Телефон или Telegram для связи:")
    await state.set_state(TradeInForm.contact)


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
