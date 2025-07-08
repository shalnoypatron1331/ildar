from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def main_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='💻 Обслуживание', callback_data='service')
    builder.button(text='🔁 Trade-in / Выкуп', callback_data='tradein')
    builder.button(text='🎁 Увеличить гарантию', callback_data='warranty')
    builder.button(text='🗺 Как добраться', callback_data='directions')
    builder.button(text='📢 Связаться с человеком', callback_data='contact')
    builder.adjust(1)
    return builder.as_markup()


def service_menu() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='🔥 Что делать, чтобы ноутбук не сгорел?', callback_data='manual')
    builder.button(text='🛠 Записаться на ТО', callback_data='service_form')
    builder.button(text='⚙️ Апгрейд / устранение проблем', callback_data='upgrade_form')
    builder.adjust(1)
    return builder.as_markup()


def manual_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='🛠 Записаться на ТО', callback_data='service_form')
    builder.adjust(1)
    return builder.as_markup()


def directions_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(text='🗺 Открыть на Яндекс.Картах', url='https://yandex.ru/maps')
    builder.button(text='📋 Скопировать адрес', callback_data='copy_address')
    builder.adjust(1)
    return builder.as_markup()
