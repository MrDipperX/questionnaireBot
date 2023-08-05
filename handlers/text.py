from loader import bot
from db.db import PgConn
from utils.lang import phrases
from utils.constants import REGIONS_UZ
from config.config import GROUP_ID


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
            text = f"Username: @{username}\nTelefon raqami: {phone}\nMaktab: {school}\nViloyat: {region}\nText: " \
                   f"{mess_text}"
            bot.delete_message(user_id, message.message_id - 1)
            bot.send_message(GROUP_ID, text)
            bot.send_message(user_id, phrases[lang]['Have'])
            db.update_user_data(['temp'], ['result'], user_id)

    except Exception as e:
        print(e)
