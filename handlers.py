from telebot import TeleBot
from config.config import TOKEN, phrases, GROUP_ID
from config.constants import SCHOOLS, REGIONS_UZ, REGIONS_KR, REGIONS_RU
from button import phone_button, regions_buttons, schools_buttons, question_button, back_keyboard, lang_buttons
from db.db import PgConn
from utils.hash_sum import hash_sum
from report import get_report_by_region, get_report_by_school, get_all_report


bot = TeleBot(token=TOKEN)


@bot.message_handler(commands=['start'])
def start_handle(message):
    db = PgConn()
    user_id = message.from_user.id
    db.add_user(user_id, message.from_user.username, message.date)

    if db.get_user_data(['temp'], user_id) == 'result':
        lang = db.get_user_data(['lang'], user_id)
        bot.send_message(user_id, phrases[lang]['Have'])
    else:
        db.update_user_data(['temp'], ['start'], user_id)
        bot.send_message(user_id, f"🇺🇿 Assalomu alaykum, tilni tanlang\n\n🇷🇺 Здарвствуйте, выберите язык"
                                  f"\n\n🇺🇿 Assalawma aleykum, tildi saylań ",
                         reply_markup=lang_buttons())


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
            lang = db.get_user_data(['lang'], user_id)
            bot.send_message(user_id, phrases[lang]['Region'], reply_markup=regions_buttons(lang))
            db.update_user_data(['temp'], ['choose_region'], user_id)

    except Exception as e:
        print(e)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        db = PgConn()
        user_id = call.message.chat.id
        lang = db.get_user_data(['lang'], user_id)

        if db.get_user_data(['temp'], user_id) == 'choose_region' and call.data != 'back':
            if lang == 'uz':
                regions = REGIONS_UZ
            elif lang == 'ru':
                regions = REGIONS_RU
            else:
                regions = REGIONS_KR

            if call.data in list(regions.keys()):
                db.update_user_data(['region'], [call.data], user_id)
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text=f"{phrases[lang]['School']}", reply_markup=schools_buttons(call.data, lang))
                db.update_user_data(['temp'], ['choose_school'], user_id)

        elif db.get_user_data(['temp'], user_id) == 'choose_school' and \
                call.data in list(SCHOOLS[db.get_user_data(['region'], user_id)]):
            db.update_user_data(['school'], [call.data], user_id)
            quest_text = db.get_question_text(1, lang)
            bot.edit_message_text(chat_id=user_id, message_id=call.message.id,
                                  text="1."+quest_text, reply_markup=question_button(lang))
            db.update_user_data(['temp'], ['question_1'], user_id)

        elif db.get_user_data(['temp'], user_id) == 'start' and call.data == 'uz':
            db.update_user_data(['lang'], ['uz'], user_id)
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(chat_id=user_id,
                             text=phrases['uz']['ComeToQuestions']+"\n\nTelefon raqamingingizni qoldiring",
                             reply_markup=phone_button(lang))

        elif db.get_user_data(['temp'], user_id) == 'start' and call.data == 'ru':
            db.update_user_data(['lang'], ['ru'], user_id)
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(chat_id=user_id,
                             text=phrases['ru']['ComeToQuestions']+"\n\nВведите номер телефона",
                             reply_markup=phone_button(lang))

        elif db.get_user_data(['temp'], user_id) == 'start' and call.data == 'kr':
            db.update_user_data(['lang'], ['kr'], user_id)
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(chat_id=user_id,
                             text=phrases['kr']['ComeToQuestions']+"\n\nTelefon nomeringingizni qaldıring",
                             reply_markup=phone_button(lang))

        elif call.data in ['1', '2', '3', '4', '5']:
            user_temp = db.get_user_data(['temp'], user_id)
            question_number = int(user_temp[-1])
            hashsum = hash_sum([question_number, user_id])
            db.add_user_choice(question_number, user_id, call.data, hashsum)

            quest_text = db.get_question_text(question_number, lang)

            if user_temp == 'question_1':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="2."+quest_text, reply_markup=question_button(lang))
                db.update_user_data(['temp'], ['question_2'], user_id)

            elif user_temp == 'question_2':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="3."+quest_text, reply_markup=question_button(lang))
                db.update_user_data(['temp'], ['question_3'], user_id)

            elif user_temp == 'question_3':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="4."+quest_text, reply_markup=question_button(lang))
                db.update_user_data(['temp'], ['question_4'], user_id)

            elif user_temp == 'question_4':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text="5."+quest_text, reply_markup=question_button(lang))
                db.update_user_data(['temp'], ['question_5'], user_id)

            elif user_temp == 'question_5':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text=phrases[lang]['Additional_question'], reply_markup=back_keyboard(lang))
                db.update_user_data(['temp'], ['open_quest'], user_id)

        elif call.data == 'back':
            user_temp = db.get_user_data(['temp'], user_id)
            if user_temp == 'choose_region':
                bot.delete_message(user_id, call.message.message_id)
                db.update_user_data(['temp'], ['start'], user_id)
                bot.send_message(user_id, f"{phrases[lang]['ComeToQuestions'].split('.')[1]}",
                                 reply_markup=phone_button(lang))

            elif user_temp == 'choose_school':
                bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                      text=f"{phrases[lang]['Region']}", reply_markup=regions_buttons(lang))
                db.update_user_data(['temp'], ['choose_region'], user_id)

            elif user_temp in ['question_1', 'question_2', 'question_3', 'question_4', 'question_5', 'open_quest']:

                if user_temp == 'question_1':
                    region = db.get_user_data(['region'], user_id)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=f"{phrases[lang]['School']}", reply_markup=schools_buttons(region, lang))
                    db.update_user_data(['temp'], ['choose_school'], user_id)
                elif user_temp == 'question_2':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number, lang)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button(lang))
                    db.update_user_data(['temp'], ['question_1'], user_id)
                elif user_temp == 'question_3':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number, lang)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button(lang))
                    db.update_user_data(['temp'], ['question_2'], user_id)
                elif user_temp == 'question_4':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number, lang)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button(lang))
                    db.update_user_data(['temp'], ['question_3'], user_id)
                elif user_temp == 'question_5':
                    question_number = int(user_temp[-1]) - 1
                    quest_text = db.get_question_text(question_number, lang)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(question_number)+"."+quest_text, reply_markup=question_button(lang))
                    db.update_user_data(['temp'], ['question_4'], user_id)
                elif user_temp == 'open_quest':
                    quest_text = db.get_question_text(5, lang)
                    bot.edit_message_text(chat_id=user_id, message_id=call.message.message_id,
                                          text=str(5) + "." + quest_text, reply_markup=question_button(lang))
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
            username, phone, school, region, lang = db.get_user_info_for_group(user_id)

            region = REGIONS_UZ[region]
            text = f"Username: @{username}\nTelefon raqami: {phone}\nMaktab: {school}\nViloyat: {region}\nText: {mess_text}"
            bot.delete_message(user_id, message.message_id - 1)
            bot.send_message(GROUP_ID, text)
            bot.send_message(user_id, phrases[lang]['Have'])
            db.update_user_data(['temp'], ['result'], user_id)

    except Exception as e:
        print(e)



