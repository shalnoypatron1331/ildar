from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from sqlalchemy.ext.asyncio import AsyncSession

from db.models import ServiceRequest, TradeInRequest, Feedback
from utils.logger import log_user_action
from keyboards.main import main_menu, manual_kb

router = Router()


class ServiceStates(StatesGroup):
    name = State()
    phone = State()
    time = State()


class TradeInStates(StatesGroup):
    manufacturer = State()
    model = State()
    photo1 = State()
    photo2 = State()
    contact = State()


class FeedbackStates(StatesGroup):
    screenshot = State()
    order_info = State()
    contact = State()


async def save_service(session: AsyncSession, data: dict, category: str) -> None:
    session.add(ServiceRequest(
        name=data['name'],
        phone=data['phone'],
        preferred_time=data['time'],
        category=category,
    ))
    await session.commit()


async def save_tradein(session: AsyncSession, data: dict) -> None:
    session.add(TradeInRequest(**data))
    await session.commit()


async def save_feedback(session: AsyncSession, data: dict) -> None:
    session.add(Feedback(**data))
    await session.commit()


@router.callback_query(F.data == 'service_form')
async def start_service_form(call: CallbackQuery, state: FSMContext):
    await call.message.answer('Введите ваше имя:')
    await state.update_data(category='maintenance')
    await state.set_state(ServiceStates.name)
    await call.answer()
    log_user_action(call.from_user.id, 'service_form', call.from_user.username)


@router.callback_query(F.data == 'upgrade_form')
async def start_upgrade_form(call: CallbackQuery, state: FSMContext):
    await call.message.answer(
        '🧩 Хотите ускорить ноутбук, увеличить объём памяти или устранить проблемы?\n\n'
        'Мы проведём бесплатную диагностику и подскажем, как можно улучшить ваш ноутбук.\n\n'
        '📌 Доступна бесплатная консультация по промокоду "UPGRADE2025".'
    )
    await call.message.answer('Введите ваше имя:')
    await state.update_data(category='upgrade')
    await state.set_state(ServiceStates.name)
    await call.answer()
    log_user_action(call.from_user.id, 'upgrade_form', call.from_user.username)


@router.message(ServiceStates.name)
async def service_name(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    category = data.get('category', 'maintenance')
    await state.update_data(name=message.text, category=category)
    await message.answer('Телефон или Telegram:')
    await state.set_state(ServiceStates.phone)
    log_user_action(message.from_user.id, 'name_entered', message.from_user.username)


@router.message(ServiceStates.phone)
async def service_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await message.answer('Удобное время для связи:')
    await state.set_state(ServiceStates.time)
    log_user_action(message.from_user.id, 'phone_entered', message.from_user.username)


@router.message(ServiceStates.time)
async def service_time(message: Message, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    data['time'] = message.text
    category = data.get('category', 'maintenance')
    await save_service(session, data, category)
    await message.answer('✅ Ваша заявка на ТО принята! Мы свяжемся с вами в ближайшее время.', reply_markup=main_menu())
    await state.clear()
    log_user_action(message.from_user.id, 'service_form_complete', message.from_user.username)


@router.callback_query(F.data == 'manual')
async def show_manual(call: CallbackQuery):
    text = (
        '💡 Полезно знать!\n\n'
        'Все ноутбуки содержат термоинтерфейс (термопасту), который со временем высыхает. Это приводит к перегреву системы, деградации чипов и в итоге — к поломке.\n\n'
        '➤ Также внутри скапливаются пыль, волосы и грязь, которые мешают охлаждению.\n\n'
        '🔁 Чтобы избежать проблем, проходите Техническое обслуживание (ТО) каждые 6 месяцев.'
    )
    await call.message.answer(text, reply_markup=manual_kb())
    await call.answer()
    log_user_action(call.from_user.id, 'manual', call.from_user.username)


@router.callback_query(F.data == 'tradein')
async def start_tradein(call: CallbackQuery, state: FSMContext):
    text = (
        '🔁 Хотите сдать старый ноутбук и получить скидку на новый?\n\n'
        'Мы принимаем технику в любом состоянии. Цена выкупа — выше рыночной. Официальные партнёры Авито.\n\n'
        '✅ Выкуп в течение 1 дня после заявки\n🎁 При сдаче техники — получите 2 подарка на выбор (мышка, сумка, подставка и др.)'
    )
    await call.message.answer(text)
    await call.message.answer('Производитель:')
    await state.set_state(TradeInStates.manufacturer)
    await call.answer()
    log_user_action(call.from_user.id, 'tradein', call.from_user.username)


@router.message(TradeInStates.manufacturer)
async def tradein_manufacturer(message: Message, state: FSMContext):
    await state.update_data(manufacturer=message.text)
    await message.answer('Модель:')
    await state.set_state(TradeInStates.model)
    log_user_action(message.from_user.id, 'manufacturer_entered', message.from_user.username)


@router.message(TradeInStates.model)
async def tradein_model(message: Message, state: FSMContext):
    await state.update_data(model=message.text)
    await message.answer('Фото 1 — внешняя крышка:')
    await state.set_state(TradeInStates.photo1)
    log_user_action(message.from_user.id, 'model_entered', message.from_user.username)


@router.message(TradeInStates.photo1, F.photo)
async def tradein_photo1(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo1=photo)
    await message.answer('Фото 2 — наклейка с моделью:')
    await state.set_state(TradeInStates.photo2)
    log_user_action(message.from_user.id, 'photo1_uploaded', message.from_user.username)


@router.message(TradeInStates.photo2, F.photo)
async def tradein_photo2(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(photo2=photo)
    await message.answer('Контакт (телефон или Telegram):')
    await state.set_state(TradeInStates.contact)
    log_user_action(message.from_user.id, 'photo2_uploaded', message.from_user.username)


@router.message(TradeInStates.contact)
async def tradein_contact(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await save_tradein(session, data)
    await message.answer('✅ Заявка отправлена! Менеджер свяжется с вами.', reply_markup=main_menu())
    await state.clear()
    log_user_action(message.from_user.id, 'tradein_complete', message.from_user.username)


@router.callback_query(F.data == 'warranty')
async def start_warranty(call: CallbackQuery, state: FSMContext):
    text = (
        '🎁 Хотите продлить гарантию?\n\n'
        'Каждый отзыв на Авито или Яндекс увеличивает гарантию на 10 дней!\n\n'
        '📷 Пришлите скриншот отзыва\n📦 Укажите номер заказа или модель ноутбука\n📞 И оставьте ваш контакт'
    )
    await call.message.answer(text)
    await call.message.answer('Пришлите скриншот:')
    await state.set_state(FeedbackStates.screenshot)
    await call.answer()
    log_user_action(call.from_user.id, 'warranty', call.from_user.username)


@router.message(FeedbackStates.screenshot, F.photo)
async def feedback_screenshot(message: Message, state: FSMContext):
    photo = message.photo[-1].file_id
    await state.update_data(screenshot=photo)
    await message.answer('Номер заказа или модель ноутбука:')
    await state.set_state(FeedbackStates.order_info)
    log_user_action(message.from_user.id, 'screenshot_uploaded', message.from_user.username)


@router.message(FeedbackStates.order_info)
async def feedback_order(message: Message, state: FSMContext):
    await state.update_data(order_info=message.text)
    await message.answer('Телефон или Telegram:')
    await state.set_state(FeedbackStates.contact)
    log_user_action(message.from_user.id, 'order_entered', message.from_user.username)


@router.message(FeedbackStates.contact)
async def feedback_contact(message: Message, state: FSMContext, session: AsyncSession):
    await state.update_data(contact=message.text)
    data = await state.get_data()
    await save_feedback(session, data)
    await message.answer('✅ Гарантия будет увеличена после подтверждения отзыва.', reply_markup=main_menu())
    await state.clear()
    log_user_action(message.from_user.id, 'feedback_complete', message.from_user.username)
