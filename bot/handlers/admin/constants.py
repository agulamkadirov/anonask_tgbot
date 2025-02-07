from aiogram.types import (
    ReplyKeyboardMarkup, KeyboardButton
)


BTN_GET_STATS_CMND = "Statistika"
BTN_SEND_MESSAGE_CMND = "Xabar yuborish"
BTN_CANCEL_CMND = "Bekor qilish"


ADMIN_MENU = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_SEND_MESSAGE_CMND)],
        [KeyboardButton(text=BTN_GET_STATS_CMND)]
    ],
    resize_keyboard=True,
)

BTN_CANCEL = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=BTN_CANCEL_CMND)],
    ],
    resize_keyboard=True,
)
