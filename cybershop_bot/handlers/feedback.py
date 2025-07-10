from aiogram import Router, F
from aiogram.types import Message, PhotoSize, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from sqlalchemy.ext.asyncio import AsyncSession

from ..db.operations import create_feedback
from ..utils.storage import save_file
from ..utils.notifications import send_notifications
from cybershop_bot.config import Settings
from ..keyboards.menu import (
    to_menu_kb,
    contact_choice_kb,
    manual_contact_kb,
    back_menu_kb,
    cancel_kb,
    with_cancel,
)

router = Router()

FEEDBACK_THANKS = (
    "\U0001F4CC \u0411\u043b\u0430\u0433\u043e\u0434\u0430\u0440\u0438\u043c \u0437\u0430 \u043e\u0442\u0437\u044b\u0432!\n\n"
    "\u041e\u0441\u0442\u0430\u043b\u0438\u0441\u044c \u0432\u043e\u043f\u0440\u043e\u0441\u044b?\n"
    "\U0001F9D1\u200D\U0001F4BB \u041d\u0430\u043f\u0438\u0448\u0438\u0442\u0435 \u043d\u0430\u043c: @CyberShop7\n"
    "\U0001F4DE \u041f\u043e\u0437\u0432\u043e\u043d\u0438\u0442\u0435: +7 977 756-92-68 (\u0418\u043b\u044c\u0434\u0430\u0440)\n"
    "\U0001F4DE \u0418\u043b\u0438: +7 977 296-12-74 (\u0410\u043b\u044c\u0431\u0435\u0440\u0442)"
)


class FeedbackForm(StatesGroup):
    screenshot = State()
    order = State()
    contact = State()


@router.callback_query(F.data == "feedback_form")
async def start_feedback(callback: CallbackQuery, state: FSMContext) -> None:
    await callback.message.delete()
    await callback.message.answer(
        "Прикрепите скрин отзыва",
        reply_markup=cancel_kb(),
    )
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
    await message.answer("Модель или номер заказа:", reply_markup=cancel_kb())
    await state.set_state(FeedbackForm.order)


@router.message(FeedbackForm.order)
async def process_order(message: Message, state: FSMContext) -> None:
    await state.update_data(order=message.text)
    await message.delete()
    await message.answer(
        "\U0001F4F1 \u041f\u043e\u0434\u0442\u0432\u0435\u0440\u0434\u0438\u0442\u0435 \u043a\u043e\u043d\u0442\u0430\u043a\u0442 \u0434\u043b\u044f \u0441\u0432\u044f\u0437\u0438:",
        reply_markup=with_cancel(contact_choice_kb()),
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
    contact = f"@{username}" if username else str(callback.from_user.id)
    await state.update_data(contact=contact)
    await callback.message.delete()
    await _finalize_feedback(callback.message, state, session, bot, settings)
    await callback.answer()


@router.callback_query(FeedbackForm.contact, F.data == "enter_contact")
async def ask_manual_contact_feedback(callback: CallbackQuery) -> None:
    await callback.message.edit_text(
        "Телефон или Telegram:",
        reply_markup=with_cancel(manual_contact_kb()),
    )
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
    await message.answer(FEEDBACK_THANKS, reply_markup=back_menu_kb())
