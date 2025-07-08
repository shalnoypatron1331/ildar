from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import User
from utils.logger import log_user_action
from keyboards.main import main_menu, service_menu, directions_kb

router = Router()


async def ensure_user(session: AsyncSession, message: Message) -> None:
    stmt = await session.execute(
        User.__table__.select().where(User.telegram_id == message.from_user.id)
    )
    user = stmt.fetchone()
    if not user:
        session.add(User(telegram_id=message.from_user.id, username=message.from_user.username))
        await session.commit()


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext, session: AsyncSession):
    await state.clear()
    await ensure_user(session, message)
    await message.answer('📋 Главное меню:\nВыберите интересующий вас раздел 👇', reply_markup=main_menu())
    log_user_action(message.from_user.id, '/start', message.from_user.username)


@router.callback_query(F.data == 'service')
async def show_service(call: CallbackQuery):
    await call.message.answer('Выберите раздел обслуживания:', reply_markup=service_menu())
    await call.answer()
    log_user_action(call.from_user.id, 'service', call.from_user.username)


@router.callback_query(F.data == 'directions')
async def show_directions(call: CallbackQuery):
    text = '📍 Адрес: Москва, ул. Примерная, д. 5, офис 21\n🚇 Ближайшее метро: Технопарк\n🕒 Мы работаем ежедневно с 10:00 до 20:00'
    await call.message.answer(text, reply_markup=directions_kb())
    await call.answer()
    log_user_action(call.from_user.id, 'directions', call.from_user.username)


@router.callback_query(F.data == 'contact')
async def contact_human(call: CallbackQuery):
    await call.message.answer('Если вы не нашли нужный раздел — напишите напрямую нашему менеджеру 👇\n@cybershop_support')
    await call.answer()
    log_user_action(call.from_user.id, 'contact', call.from_user.username)


@router.message()
async def any_text(message: Message, state: FSMContext):
    if state.get_state() is None:
        await message.delete()
        await message.answer('Пожалуйста, используйте кнопки')
        log_user_action(message.from_user.id, 'text_removed', message.from_user.username)
