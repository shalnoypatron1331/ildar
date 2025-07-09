from aiogram import Router, F
from aiogram.types import Message, PhotoSize, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import create_feedback
from ..utils.storage import save_file
from ..utils.notifications import send_notifications
from cybershop_bot.config import Settings
from ..keyboards.menu import to_menu_kb

router = Router()


class FeedbackForm(StatesGroup):
    screenshot = State()
    order = State()
    contact = State()


@router.callback_query(F.data == "feedback_form")
async def start_feedback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer("Прикрепите скрин отзыва")
    await state.set_state(FeedbackForm.screenshot)
    await callback.answer()


@router.message(FeedbackForm.screenshot)
async def process_screenshot(message: Message, state: FSMContext) -> None:
    if not message.photo:
        await message.answer("Нужен скрин")
        return
    photo: PhotoSize = message.photo[-1]
    filename = f"{message.from_user.id}_screenshot.jpg"
    downloaded = await photo.download()
    path = save_file(downloaded, filename, 'feedback')
    await state.update_data(screenshot=path)
    await message.delete()
    await message.answer("Модель или номер заказа:")
    await state.set_state(FeedbackForm.order)


@router.message(FeedbackForm.order)
async def process_order(message: Message, state: FSMContext) -> None:
    await state.update_data(order=message.text)
    await message.delete()
    await message.answer("Телефон или Telegram:")
    await state.set_state(FeedbackForm.contact)


@router.message(FeedbackForm.contact)
async def finish_feedback(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    await state.update_data(contact=message.text)
    await message.delete()
    data = await state.get_data()
    fb = await create_feedback(
        session,
        order_info=data["order"],
        contact=data["contact"],
        screenshot=data["screenshot"],
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
        "\u2705 Спасибо! Ваша заявка принята. Мы свяжемся с вами в течение дня.",
        reply_markup=to_menu_kb(),
    )
