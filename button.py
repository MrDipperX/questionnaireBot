from telebot import types
from config.config import phrases
from config.constants import REGIONS, SCHOOLS


def phone_button():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    telp_numb_btn = types.KeyboardButton(f"📱 {phrases['Telp_numb_button']}", request_contact=True)
    keyboard.add(telp_numb_btn)

    return keyboard


def regions_buttons():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(value, callback_data=f'{key}') for key, value in REGIONS.items()]
    keyboard.add(*buttons)
    back = types.InlineKeyboardButton(f"⬅ {phrases['Back']}", callback_data='back')
    keyboard.add(back)

    return keyboard


def schools_buttons(region):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(value, callback_data=f'{value}') for value in SCHOOLS[region]]
    keyboard.add(*buttons)
    back = types.InlineKeyboardButton(f"⬅ {phrases['Back']}", callback_data='back')
    keyboard.add(back)

    return keyboard


def question_button():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton("⭐️" * value, callback_data=value) for value in range(1, 6)]
    keyboard.add(*buttons)
    back = types.InlineKeyboardButton(f"⬅ {phrases['Back']}", callback_data='back')
    keyboard.add(back)

    return keyboard


def back_keyboard():
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(f"⬅ {phrases['Back']}", callback_data='back')
    keyboard.add(back)
    return keyboard

