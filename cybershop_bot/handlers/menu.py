from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command

from ..keyboards.menu import (
    start_kb,
    main_menu_kb,
    service_menu_kb,
    tradein_kb,
    feedback_kb,
    location_kb,
    contact_kb,
    to_menu_kb,
    back_service_kb,
)

router = Router()

WELCOME_TEXT = (
    "Привет! \U0001F44B\n"
    "Я — бот CYBERSHOP. Помогу тебе быстро решить любой вопрос о ноутбуках.\n\n"
    "Нажми кнопку ниже, чтобы начать \u2B07\uFE0F"
)

MENU_TEXT = "\U0001F4CB Главное меню:\nВыберите интересующий вас раздел \u2B07\uFE0F"
SERVICE_INFO = (
    "\U0001F525 Важно знать!\n\n"
    "Все ноутбуки содержат термоинтерфейс (термопасту), который со временем теряет свойства. Это ведёт к перегреву, снижению производительности и поломке.\n"
    "Также в систему попадают пыль, волосы, грязь — они ухудшают охлаждение.\n\n"
    "\U0001F501 Рекомендуем проходить ТО раз в 6 месяцев.\n\n"
    "\u2B07\uFE0F Хотите записаться?"
)
UPGRADE_INFO = (
    "\u2699\uFE0F Хотите ускорить ноутбук, увеличить память или устранить проблемы?\n\n"
    "Проведём диагностику, подберём апгрейд и бесплатно проконсультируем.\n\n"
    "\U0001F4A1 Промокод: UPGRADE2025 — диагностика бесплатно!"
)
TRADEIN_INFO = (
    "\U0001F501 Хотите обменять старый ноутбук на новый?\n\n"
    "Мы выкупаем любую технику в течение 1 дня. Цена — выше средней по рынку.\n"
    "\U0001F381 При сдаче техники — выберите 2 подарка (мышка, коврик, сумка и др.)\n\n"
    "\u2B07\uFE0F Оставьте заявку:"
)
FEEDBACK_INFO = (
    "\U0001F381 Хотите увеличить гарантию на 10 дней?\n\n"
    "1. Оставьте отзыв на Яндексе или Авито\n"
    "2. Пришлите скриншот\n"
    "3. Укажите модель ноутбука или номер заказа\n"
    "4. Оставьте телефон или Telegram\n\n"
    "После проверки гарантия будет продлена."
)
LOCATION_TEXT = (
    "\U0001F4CD Мы находимся по адресу:\n"
    "Москва, ул. Примерная, д. 5, офис 21\n"
    "\U0001F687 Метро Технопарк\n"
    "\U0001F553 Ежедневно с 10:00 до 20:00"
)
CONTACT_TEXT = (
    "\U0001F64B\u200D♂️ Не нашли нужную информацию?\n\n"
    "Напишите нам напрямую: @cybershop_support"
)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    await message.answer(WELCOME_TEXT, reply_markup=start_kb())
    await message.delete()


@router.callback_query(F.data == "menu")
async def show_menu(callback: CallbackQuery) -> None:
    await callback.message.delete()
    await callback.message.answer(MENU_TEXT, reply_markup=main_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "service")
async def service_menu(callback: CallbackQuery) -> None:
    await callback.message.edit_text(MENU_TEXT, reply_markup=service_menu_kb())
    await callback.answer()


@router.callback_query(F.data == "heat_info")
async def heat_info(callback: CallbackQuery) -> None:
    await callback.message.edit_text(SERVICE_INFO, reply_markup=back_service_kb())
    await callback.answer()


@router.callback_query(F.data == "upgrade")
async def upgrade_info(callback: CallbackQuery) -> None:
    await callback.message.edit_text(UPGRADE_INFO, reply_markup=back_service_kb())
    await callback.answer()


@router.callback_query(F.data == "tradein")
async def tradein_info(callback: CallbackQuery) -> None:
    await callback.message.edit_text(TRADEIN_INFO, reply_markup=tradein_kb())
    await callback.answer()


@router.callback_query(F.data == "feedback")
async def feedback_info(callback: CallbackQuery) -> None:
    await callback.message.edit_text(FEEDBACK_INFO, reply_markup=feedback_kb())
    await callback.answer()


@router.callback_query(F.data == "location")
async def location_info(callback: CallbackQuery) -> None:
    await callback.message.edit_text(LOCATION_TEXT, reply_markup=location_kb())
    await callback.answer()


@router.callback_query(F.data == "contact")
async def contact_info(callback: CallbackQuery) -> None:
    await callback.message.edit_text(CONTACT_TEXT, reply_markup=contact_kb())
    await callback.answer()


@router.callback_query(F.data == "copy_addr")
async def copy_addr(callback: CallbackQuery) -> None:
    await callback.answer("Адрес скопирован")
    await callback.message.answer("Москва, ул. Примерная, д. 5, офис 21")
