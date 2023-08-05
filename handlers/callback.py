from loader import bot
from db.db import PgConn
from utils.lang import phrases
from keyboards.button import schools_buttons, regions_buttons, question_button, phone_button, back_keyboard
from utils.hash_sum import hash_sum
from utils.constants import REGIONS_UZ, REGIONS_RU, REGIONS_KR, SCHOOLS


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    try:
        db = PgConn()
        user_id = call.message.chat.id

        if db.get_user_data(['temp'], user_id) == 'choose_region' and call.data != 'back':
            lang = db.get_user_data(['lang'], user_id)
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
            lang = db.get_user_data(['lang'], user_id)
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
                             reply_markup=phone_button('uz'))

        elif db.get_user_data(['temp'], user_id) == 'start' and call.data == 'ru':
            db.update_user_data(['lang'], ['ru'], user_id)
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(chat_id=user_id,
                             text=phrases['ru']['ComeToQuestions']+"\n\nВведите номер телефона",
                             reply_markup=phone_button('ru'))

        elif db.get_user_data(['temp'], user_id) == 'start' and call.data == 'kr':
            db.update_user_data(['lang'], ['kr'], user_id)
            bot.delete_message(user_id, call.message.message_id)
            bot.send_message(chat_id=user_id,
                             text=phrases['kr']['ComeToQuestions']+"\n\nTelefon nomeringingizni qaldıring",
                             reply_markup=phone_button('kr'))

        elif call.data in ['1', '2', '3', '4', '5']:
            lang = db.get_user_data(['lang'], user_id)
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
            lang = db.get_user_data(['lang'], user_id)
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
