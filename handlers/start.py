from loader import bot
from db.db import PgConn
from utils.lang import phrases
from keyboards.button import lang_buttons


@bot.message_handler(commands=['start'])
def start_handle(message):
    db = PgConn()
    user_id = message.from_user.id
    db.add_user(user_id, message.from_user.username)

    if db.get_user_data(['temp'], user_id) == 'result':
        lang = db.get_user_data(['lang'], user_id)
        bot.send_message(user_id, phrases[lang]['Have'])
    else:
        db.update_user_data(['temp'], ['start'], user_id)
        bot.send_message(user_id, f"🇺🇿 Assalomu alaykum, tilni tanlang\n\n🇷🇺 Здарвствуйте, выберите язык"
                                  f"\n\n🇺🇿 Assalawma aleykum, tildi saylań ",
                         reply_markup=lang_buttons())
