from telebot import TeleBot
from config.config import TOKEN, phrases, GROUP_ID
from config.constants import SCHOOLS, REGIONS
from button import phone_button, regions_buttons, schools_buttons, question_button, back_keyboard
from db.db import PgConn
from utils.hash_sum import hash_sum
from report import get_report_by_region, get_report_by_school, get_all_report
import time

bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start_handle(message):
    db = PgConn()
    user_id = message.from_user.id
    db.add_user(user_id, message.from_user.username, message.date)

    if db.get_user_data(['temp'], user_id) == 'result':
        bot.send_message(user_id, phrases['Have'])
    else:
        db.update_user_data(['temp'], ['start'], user_id)
        hello = phrases['Hello'].split(',')[0]
        telp_numb = phrases['Hello'].split(',')[1]

        bot.send_message(user_id, f"{phrases['ComeToQuestions']}")
        bot.send_message(user_id, f"{hello}, {message.from_user.first_name}{telp_numb}",
                         reply_markup=phone_button())


@bot.message_handler(commands=['school'])
def get_school_xlsx(message):
    try:
        get_report_by_school()
        xlsx_file = open("files/report_school.xlsx", "rb")
        bot.send_document(message.from_user.id, xlsx_file)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['region'])
def get_school_xlsx(message):
    try:
        get_report_by_region()
        xlsx_file = open("files/report_region.xlsx", "rb")
        bot.send_document(message.from_user.id, xlsx_file)
    except Exception as e:
        print(e)


@bot.message_handler(commands=['report'])
def get_school_xlsx(message):
    try:
        get_all_report()
        xlsx_file = open("files/report.xlsx", "rb")
        bot.send_document(message.from_user.id, xlsx_file)
    except Exception as e:
        print(e)


@bot.message_handler(content_types=['contact'])
def get_contact(message):
    try:
        db = PgConn()
        user_id = message.from_user.id

        if db.get_user_data(['temp'], user_id) == 'start':
            db.update_user_data(['phone_numb'], [message.contact.phone_number], user_id)
            bot.send_message(user_id, phrases['Region'], reply_markup=regions_buttons())
            db.update_user_data(['temp'], ['choose_region'], user_id)

    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        db = PgConn()
        user_id = call.message.chat.id

        if call.data in list(REGIONS.keys()) and db.get_user_data(['temp'], user_id) == 'choose_region':
            db.update_user_data(['region'], [call.data], user_id)
            bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                  text=f"{phrases['School']}", reply_markup=schools_buttons(call.data))
            db.update_user_data(['temp'], ['choose_school'], user_id)

        elif call.data in list(SCHOOLS[db.get_user_data(['region'], user_id)]) and \
                db.get_user_data(['temp'], user_id) == 'choose_school':
            db.update_user_data(['school'], [call.data], user_id)
            # bot.send_message(user_id, phrases['ComeToQuestions'])
            quest_text = db.get_question_text(1)
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id,
                                  text="1."+quest_text, reply_markup=question_button())
            db.update_user_data(['temp'], ['question_1'], user_id)

        elif call.data in ['1', '2', '3', '4', '5']:
            user_temp = db.get_user_data(['temp'], user_id)
            question_number = int(user_temp[-1])
            hashsum = hash_sum([question_number, user_id])
            db.add_user_choice(question_number, user_id, call.data, hashsum)

            quest_text = db.get_question_text(question_number)

            if user_temp == 'question_1':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="2."+quest_text, reply_markup=question_button())
                db.update_user_data(['temp'], ['question_2'], user_id)

            elif user_temp == 'question_2':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="3."+quest_text, reply_markup=question_button())
                db.update_user_data(['temp'], ['question_3'], user_id)

            elif user_temp == 'question_3':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="4."+quest_text, reply_markup=question_button())
                db.update_user_data(['temp'], ['question_4'], user_id)

            elif user_temp == 'question_4':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="5."+quest_text, reply_markup=question_button())
                db.update_user_data(['temp'], ['question_5'], user_id)

            elif user_temp == 'question_5':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text=phrases['Additional_question'], reply_markup=back_keyboard())
                db.update_user_data(['temp'], ['open_quest'], user_id)

        elif call.data == 'back':
            user_temp = db.get_user_data(['temp'], user_id)
            if user_temp == 'choose_region':
                bot.delete_message(user_id, call.message.message_id)
                db.update_user_data(['temp'], ['start'], user_id)
                bot.send_message(user_id, f"{phrases['Hello'].split('.')[1]}", reply_markup=phone_button())

            elif user_temp == 'choose_school':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text=f"{phrases['Region']}", reply_markup=regions_buttons())
                db.update_user_data(['temp'], ['choose_region'], user_id)

            elif user_temp in ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'open_quest']:

                if user_temp == 'question_1':
                    region = db.get_user_data(['region'], user_id)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=f"{phrases['School']}", reply_markup=schools_buttons(region))
                    db.update_user_data(['temp'], ['choose_school'], user_id)
                elif user_temp == 'question_2':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button())
                    db.update_user_data(['temp'], ['question_1'], user_id)
                elif user_temp == 'question_3':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button())
                    db.update_user_data(['temp'], ['question_2'], user_id)
                elif user_temp == 'question_4':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button())
                    db.update_user_data(['temp'], ['question_3'], user_id)
                elif user_temp == 'question_5':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button())
                    db.update_user_data(['temp'], ['question_4'], user_id)
                elif user_temp == 'open_quest':
                    quest_text = db.get_question_text(5)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(5) + "." + quest_text, reply_markup=question_button())
                    db.update_user_data(['temp'], ['question_5'], user_id)

    except Exception as e:
        print(e)


@bot.message_handler(content_types=['text'])
def text_handle(message):
    try:
        db = PgConn()
        user_id = message.chat.id
        mess_text = message.text.strip()

        user_temp = db.get_user_data(['temp'], user_id)

        if user_temp == 'open_quest':
            username, phone, school, region = db.get_user_info_for_group(user_id)
            region = REGIONS[region]
            text = f"Username: @{username}\nTelefon raqami: {phone}\nMaktab: {school}\nViloyat: {region}\nText: {mess_text}"
            bot.send_message(GROUP_ID, text)
            db.update_user_data(['temp'], ['result'], user_id)

    except Exception as e:
        print(e)



