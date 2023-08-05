from config.config import GROUP_ID
from utils.constants import SCHOOLS, REGIONS_UZ, REGIONS_KR, REGIONS_RU
from keyboards.button import phone_button, regions_buttons, schools_buttons, question_button, back_keyboard, lang_buttons
from db.db import PgConn
from utils.hash_sum import hash_sum
from utils.report import get_report_by_region, get_report_by_school, get_all_report
from loader import bot
from utils.lang import phrases


@bot.message_handler(commands=['school'])
def get_school_xlsx(message):
    try:
        empty = get_report_by_school()
        user_id = message.from_user.id
        if empty == "Empty":
            db = PgConn()
            lang = db.get_user_data(['lang'], user_id)
            lang = 'uz' if lang is None else lang
            bot.send_message(user_id, phrases[lang]['No Data'])
        else:
            xlsx_file = open("files/report_school.xlsx", "rb")
            bot.send_document(user_id, xlsx_file)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['region'])
def get_school_xlsx(message):
    try:
        empty = get_report_by_region()
        user_id = message.from_user.id
        if empty == "Empty":
            db = PgConn()
            lang = db.get_user_data(['lang'], user_id)
            lang = 'uz' if lang is None else lang
            bot.send_message(user_id, phrases[lang]['No Data'])
        else:
            xlsx_file = open("files/report_region.xlsx", "rb")
            bot.send_document(user_id, xlsx_file)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['report'])
def get_school_xlsx(message):
    try:
        empty = get_all_report()
        user_id = message.from_user.id
        if empty == "Empty":
            db = PgConn()
            lang = db.get_user_data(['lang'], user_id)
            lang = 'uz' if lang is None else lang
            bot.send_message(user_id, phrases[lang]['No Data'])
        else:
            xlsx_file = open("../files/report.xlsx", "rb")
            bot.send_document(user_id, xlsx_file)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    try:
        db = PgConn()
        user_id = message.from_user.id

        if db.get_user_data(['temp'], user_id) == 'start':
            db.update_user_data(['phone_numb'], [message.contact.phone_number], user_id)
            lang = db.get_user_data(['lang'], user_id)
            bot.send_message(user_id, phrases[lang]['Region'], reply_markup=regions_buttons(lang))
            db.update_user_data(['temp'], ['choose_region'], user_id)

    except Exception as e:
        print(e)
