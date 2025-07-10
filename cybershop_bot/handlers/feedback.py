from aiogram import Router, F
from aiogram.types import Message, PhotoSize, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import create_feedback
from ..utils.storage import save_file
from ..utils.notifications import send_notifications
from cybershop_bot.config import Settings
from ..keyboards.menu import to_menu_kb, contact_choice_kb

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
    await message.answer(
        "\U0001F4F1 \u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 \u0434\u043b\u044f \u0441\u0432\u044f\u0437\u0438:",
        reply_markup=contact_choice_kb(),
    )
    await state.set_state(FeedbackForm.contact)


@router.callback_query(FeedbackForm.contact, F.data == "use_username")
async def autofill_contact_feedback(
    callback: CallbackQuery,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
    username = callback.from_user.username
    if not username:
        await callback.message.edit_text(
            "\u2757 \u0423 \u0432\u0430\u0441 \u043d\u0435 \u0443\u0441\u0442\u0430\u043d\u043e\u0432\u043b\u0435\u043d username \u0432 Telegram. \u041f\u043e\u0436\u0430\u043b\u0443\u0439\u0441\u0442\u0430, \u0432\u0432\u0435\u0434\u0438\u0442\u0435 \u043d\u043e\u043c\u0435\u0440 \u0440\u0443\u0447\u043d\u043e.",
            reply_markup=None,
        )
        await callback.answer()
        return
    await state.update_data(contact=f"@{username}")
    await callback.message.delete()
    await _finalize_feedback(callback.message, state, session, bot, settings)
    await callback.answer()


@router.callback_query(FeedbackForm.contact, F.data == "enter_contact")
async def ask_manual_contact_feedback(callback: CallbackQuery) -> None:
    await callback.message.edit_text("Телефон или Telegram:")
    await callback.answer()


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
    await _finalize_feedback(message, state, session, bot, settings)


async def _finalize_feedback(
    message: Message,
    state: FSMContext,
    session: AsyncSession,
    bot,
    settings: Settings,
) -> None:
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
