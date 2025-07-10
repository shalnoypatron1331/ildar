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
    contact_manager_kb,
    to_menu_kb,
    back_service_kb,
    heat_info_kb,
)

router = Router()

WELCOME_TEXT = (
    "Привет! \U0001F44B\n"
    "Я — бот CYBERSHOP. Помогу тебе быстро решить любой вопрос о ноутбуках.\n\n"
    "Нажми кнопку ниже, чтобы начать \u2B07\uFE0F"
)

MENU_TEXT = "\U0001F4CB Главное меню:\nВыберите интересующий вас раздел \u2B07\uFE0F"
SERVICE_INFO = (
    "\U0001F525 Важно знать!\n"
    "Каждый ноутбук внутри содержит термоинтерфейс (термопасту), который "
    "обеспечивает отвод тепла от процессора и видеочипа.\n"
    "Со временем термопаста высыхает и теряет свои свойства, из-за чего:\n"
    "\u26A0\uFE0F Температура компонентов растёт\n"
    "\u26A0\uFE0F Производительность падает\n"
    "\u26A0\uFE0F Устройство начинает тормозить\n"
    "\u26A0\uFE0F Повышается риск серьёзной поломки (например, отвал чипа)\n"
    "Дополнительно пыль, волосы и грязь, попадающие внутрь, забивают "
    "вентиляцию, нарушают циркуляцию воздуха и ещё сильнее ухудшают "
    "охлаждение.\n"
    "\U0001F6E1\uFE0F Регулярное техническое обслуживание (ТО) — это "
    "комплексная профилактика:\n"
    "\u2705 Замена термопасты\n"
    "\u2705 Полная очистка системы охлаждения\n"
    "\u2705 Осмотр платы, разъёмов и накопителей\n"
    "\U0001F501 Рекомендуем проходить ТО каждые 6–12 месяцев.\n"
    "Срок зависит от:\n"
    "— мощности ноутбука\n"
    "— игровых или рабочих нагрузок\n"
    "— условий эксплуатации (пыль, перегрев, работа на коленях)\n"
    "\U0001F9D1\u200D\U0001F527 Хотите продлить жизнь своему ноутбуку и "
    "сохранить его производительность?\n"
    "\u2B07\uFE0F Нажмите ниже, чтобы записаться на ТО"
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

ADDRESS_TEXT = (
    "\u041c\u043e\u0441\u043a\u0432\u0430, \u0411\u0443\u0434\u0430\u0439\u0441\u043a\u0438\u0439 \u043f\u0440\u043e\u0435\u0437\u0434, \u0434. 7, \u043a\u043e\u0440\u043f. 1, \u043f\u043e\u0434\u044a\u0435\u0437\u0434 3, \u044d\u0442\u0430\u0436 -1\n"
    "\U0001F687 \u041c\u0426\u041a \u0420\u043e\u0441\u0442\u043e\u043a\u0438\u043d\u043e\n"
    "\U0001F551 \u0435\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u043e \u0441 10:00 \u0434\u043e 20:00"
)
LOCATION_TEXT = (
    "\U0001F4CD \u041c\u044b \u043d\u0430\u0445\u043e\u0434\u0438\u043c\u0441\u044f \u043f\u043e \u0430\u0434\u0440\u0435\u0441\u0443:\n" + ADDRESS_TEXT
)
CONTACT_TEMPLATE = (
    "\U0001F4F2 \u0421\u0432\u044f\u0437\u044c \u0441 \u043c\u0435\u043d\u0435\u0434\u0436\u0435\u0440\u043e\u043c:\n\n"
    "\u0412\u044b \u043c\u043e\u0436\u0435\u0442\u0435 \u043d\u0430\u043f\u0438\u0441\u0430\u0442\u044c \u043d\u0430\u043f\u0440\u044f\u043c\u0443:\n"
    "\u2014 Telegram: @{manager}\n"
    "\u2014 \u0422\u0435\u043b\u0435\u0444\u043e\u043d: {phone}\n"
    "\u2014 \u0427\u0430\u0442 \u043f\u043e\u0434\u0434\u0435\u0440\u0436\u043a\u0438: @{support}\n\n"
    "\U0001F559 \u0412\u0440\u0435\u043c\u044F \u0440\u0430\u0431\u043e\u0442\u044b: \u0435\u0436\u0435\u0434\u043d\u0435\u0432\u043d\u043e \u0441 10:00 \u0434\u043e 20:00"
)


@router.message(Command("start"))
async def cmd_start(message: Message) -> None:
    if message.chat.type == "private":
        await message.delete()
    await message.answer(WELCOME_TEXT, reply_markup=start_kb())


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
    await callback.message.edit_text(SERVICE_INFO, reply_markup=heat_info_kb())
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


@router.callback_query(F.data == "contact_manager")
async def contact_manager(callback: CallbackQuery, settings: Settings) -> None:
    text = CONTACT_TEMPLATE.format(
        manager=settings.manager_username,
        phone=settings.manager_phone,
        support=settings.support_username,
    )
    await callback.message.edit_text(
        text,
        reply_markup=contact_manager_kb(settings.manager_username),
    )
    await callback.answer()


@router.callback_query(F.data == "copy_addr")
async def copy_addr(callback: CallbackQuery) -> None:
    await callback.message.answer(
        "\U0001F4CB \u0410\u0434\u0440\u0435\u0441:\n" + ADDRESS_TEXT
    )
    await callback.answer()
