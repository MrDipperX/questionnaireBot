from telebot import types
from config.config import phrases
from config.constants import REGIONS_KR, REGIONS_RU, REGIONS_UZ, SCHOOLS


def lang_buttons():
    keyboard = types.InlineKeyboardMarkup(row_width=3)
    uz_btn = types.InlineKeyboardButton("🇺🇿 O'zbekcha", callback_data='uz')
    ru_btn = types.InlineKeyboardButton("🇷🇺 Русский", callback_data='ru')
    kr_btn = types.InlineKeyboardButton("🇺🇿 Qaraqalpaqsha", callback_data='kr')
    keyboard.add(uz_btn, ru_btn, kr_btn)

    return keyboard


def phone_button(lang):
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2, one_time_keyboard=True)
    telp_numb_btn = types.KeyboardButton(f"📱 {phrases[lang]['Telp_numb_button']}", request_contact=True)
    keyboard.add(telp_numb_btn)

    return keyboard


def regions_buttons(lang):
    if lang == 'uz':
        regions = REGIONS_UZ
    elif lang == 'ru':
        regions = REGIONS_RU
    else:
        regions = REGIONS_KR
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(value, callback_data=f'{key}') for key, value in regions.items()]
    keyboard.add(*buttons)
    back = types.InlineKeyboardButton(f"⬅ {phrases[lang]['Back']}", callback_data='back')
    keyboard.add(back)

    return keyboard


def schools_buttons(region, lang):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton(value, callback_data=f'{value}') for value in SCHOOLS[region]]
    keyboard.add(*buttons)
    back = types.InlineKeyboardButton(f"⬅ {phrases[lang]['Back']}", callback_data='back')
    keyboard.add(back)

    return keyboard


def question_button(lang):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    buttons = [types.InlineKeyboardButton("⭐️" * value, callback_data=value) for value in range(1, 6)]
    keyboard.add(*buttons)
    back = types.InlineKeyboardButton(f"⬅ {phrases[lang]['Back']}", callback_data='back')
    keyboard.add(back)

    return keyboard


def back_keyboard(lang):
    keyboard = types.InlineKeyboardMarkup(row_width=1)
    back = types.InlineKeyboardButton(f"⬅ {phrases[lang]['Back']}", callback_data='back')
    keyboard.add(back)
    return keyboard

