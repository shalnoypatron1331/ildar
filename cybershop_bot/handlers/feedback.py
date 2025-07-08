from aiogram import Router
from aiogram.types import Message, PhotoSize
from aiogram.filters import Command
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import create_feedback
from ..utils.storage import save_file
from ..utils.notifications import send_notifications
from ..config import Settings

router = Router()


class FeedbackForm(StatesGroup):
    order = State()
    contact = State()
    screenshot = State()


@router.message(Command("feedback"))
async def start_feedback(message: Message, state: FSMContext) -> None:
    await message.answer("Товар или заказ:")
    await state.set_state(FeedbackForm.order)


@router.message(FeedbackForm.order)
async def process_order(message: Message, state: FSMContext) -> None:
    await state.update_data(order=message.text)
    await message.answer("Контакт:")
    await state.set_state(FeedbackForm.contact)


@router.message(FeedbackForm.contact)
async def process_contact(message: Message, state: FSMContext) -> None:
    await state.update_data(contact=message.text)
    await message.answer("Прикрепите скрин")
    await state.set_state(FeedbackForm.screenshot)


@router.message(FeedbackForm.screenshot)
async def finish_feedback(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    if not message.photo:
        await message.answer("Нужен скрин")
        return
    photo: PhotoSize = message.photo[-1]
    filename = f"{message.from_user.id}_screenshot.jpg"
    downloaded = await photo.download()
    path = save_file(downloaded, filename, 'feedback')
    data = await state.get_data()
    fb = await create_feedback(
        session,
        order_info=data["order"],
        contact=data["contact"],
        screenshot=path,
    )
    text = (
        "\U0001F381 Отзыв для продления гарантии:\n\n"
        f"\U0001F4E6 Товар/Заказ: {fb.order_info}\n"
        f"\U0001F4DE Контакт: {fb.contact}\n"
        f"\U0001F194 TG ID: {message.from_user.id}"
    )
    await send_notifications(bot, text, settings, photo_path=fb.screenshot)
    await state.clear()
    await message.answer(
        "\u2705 Спасибо! Ваша заявка передана. Мы свяжемся с вами в течение рабочего дня."
    )
