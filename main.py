from handlers import bot
from db.db import PgConn


if __name__ == '__main__':
    db_conn = PgConn()
    db_conn.create_tables()
    db_conn.add_init_questions()

    bot.polling(none_stop=True)
