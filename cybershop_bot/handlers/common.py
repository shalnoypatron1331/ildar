from aiogram import Router, F
from aiogram.types import CallbackQuery
from aiogram.fsm.context import FSMContext

from ..keyboards.menu import main_menu_kb

router = Router()

@router.callback_query(F.data == "cancel_form")
async def cancel_form(callback: CallbackQuery, state: FSMContext) -> None:
    await state.clear()
    await callback.message.delete()
    await callback.message.answer(
        "❗️Вы отменили заполнение формы. Возвращаемся в главное меню.",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()

@router.callback_query(F.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer(
        "\U0001F4CB Главное меню:\nВыберите интересующий вас раздел \u2B07\uFE0F",
        reply_markup=main_menu_kb(),
    )
    await callback.answer()
