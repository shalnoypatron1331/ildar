from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def start_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\U0001F680 \u041d\u0430\u0447\u0430\u0442\u044c", callback_data="menu")]]
    )


def main_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="\U0001F4BB \u041e\u0431\u0441\u043b\u0443\u0436\u0438\u0432\u0430\u043d\u0438\u0435", callback_data="service"),
                InlineKeyboardButton(text="\U0001F501 Trade-in / \u0412\u044b\u043a\u0443\u043f", callback_data="tradein"),
            ],
            [
                InlineKeyboardButton(text="\U0001F381 \u0423\u0432\u0435\u043b\u0438\u0447\u0438\u0442\u044c \u0433\u0430\u0440\u0430\u043d\u0442\u0438\u044e", callback_data="feedback"),
                InlineKeyboardButton(text="\U0001F5FA \u041a\u0430\u043a \u0434\u043e\u0431\u0440\u0430\u0442\u044c\u0441\u044f", callback_data="location"),
            ],
            [InlineKeyboardButton(text="\U0001F4E2 \u0421\u0432\u044f\u0437\u0430\u0442\u044c\u0441\u044f \u0441 \u0447\u0435\u043b\u043e\u0432\u0435\u043a\u043e\u043c", callback_data="contact")],
        ]
    )


def service_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="\U0001F525 \u0427\u0442\u043e \u0434\u0435\u043b\u0430\u0442\u044c, \u0447\u0442\u043e\u0431\u044b \u043d\u0435 \u0441\u0433\u043e\u0440\u0435\u043b?", callback_data="heat_info")],
            [InlineKeyboardButton(text="\U0001F6E0 \u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044C\u0441\u044f \u043d\u0430 \u0422\u041e", callback_data="maintenance")],
            [InlineKeyboardButton(text="\u2699\ufe0f \u0410\u043f\u0433\u0440\u0435\u0439\u0434 / \u0443\u0441\u0442\u0440\u0430\u043d\u0435\u043d\u0438\u0435 \u043f\u0440\u043e\u0431\u043b\u0435\u043c", callback_data="upgrade")],
            [InlineKeyboardButton(text="\u21a9\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="menu")],
        ]
    )


def to_menu_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\U0001F4CB \u0412\u0435\u0440\u043d\u0443\u0442\u044c\u0441\u044f \u0432 \u0433\u043b\u0430\u0432\u043d\u043e\u0435 \u043c\u0435\u043d\u044e", callback_data="menu")]]
    )


def back_service_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\u21a9\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="service")]]
    )


def heat_info_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="\U0001F6E0 \u0417\u0430\u043f\u0438\u0441\u0430\u0442\u044C\u0441\u044f \u043d\u0430 \u0422\u041E", callback_data="maintenance")],
            [InlineKeyboardButton(text="\u21a9\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="service")],
        ]
    )


def tradein_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\U0001F4E5 \u0421\u0434\u0430\u0442\u044c \u0442\u0435\u0445\u043d\u0438\u043a\u0443", callback_data="tradein_form")],
                         [InlineKeyboardButton(text="\u21a9\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="menu")]]
    )


def feedback_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\U0001F4E5 \u041e\u0442\u043f\u0440\u0430\u0432\u0438\u0442\u044c \u043e\u0442\u0437\u044b\u0432", callback_data="feedback_form")],
                         [InlineKeyboardButton(text="\u21a9\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="menu")]]
    )


def location_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="\U0001F5FA \u041e\u0442\u043a\u0440\u044b\u0442\u044c \u043d\u0430 \u042f\u043d\u0434\u0435\u043a\u0441.\u041a\u0430\u0440\u0442\u0430\u0445", url="https://yandex.ru/maps/?text=%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C%20%D1%83%D0%BB.%20%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80%D0%BD%D0%B0%D1%8F%2C%205" )],
            [InlineKeyboardButton(text="\U0001F4CB \u0421\u043a\u043e\u043f\u0438\u0440\u043e\u0432\u0430\u0442\u044c \u0430\u0434\u0440\u0435\u0441", callback_data="copy_addr")],
            [InlineKeyboardButton(text="\u21a9\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="menu")],
        ]
    )


def contact_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="\u21a9\ufe0f \u041d\u0430\u0437\u0430\u0434", callback_data="menu")]]
    )

def contact_choice_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="\U0001F464 \u0412\u0441\u0442\u0430\u0432\u0438\u0442\u044c \u043c\u043e\u0439 Telegram", callback_data="use_username")],
            [InlineKeyboardButton(text="\u270D\uFE0F \u0412\u0432\u0435\u0441\u0442\u0438 \u0432\u0440\u0443\u0447\u043d\u0443\u044e", callback_data="enter_contact")],
        ]
    )
