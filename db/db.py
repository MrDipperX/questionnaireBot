import psycopg2
from psycopg2 import sql
from datetime import datetime
from config.config import HOST, PORT, DBNAME, PASSWORD, USER
from config.constants import QUESTIONS


class PgConn:
    def __init__(self):
        self.conn = None
        try:
            self.conn = psycopg2.connect(database=DBNAME, user=USER, password=PASSWORD, host=HOST, port=PORT)
            self.cur = self.conn.cursor()

        except(Exception, psycopg2.DatabaseError, psycopg2.OperationalError) as error:
            print(error)

    def create_tables(self):
        with self.conn:
            self.cur.execute("""CREATE TABLE IF NOT EXISTS Users(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    id_tg BIGINT ,
                                    username CHARACTER VARYING(100) ,
                                    date_reg TIMESTAMP WITHOUT TIME ZONE,
                                    phone_numb CHARACTER VARYING(15),
                                    is_admin BOOLEAN DEFAULT FALSE,
                                    region CHARACTER VARYING(100),
                                    school CHARACTER VARYING(100),
                                    temp CHARACTER VARYING(50))""")
            self.conn.commit()

            self.cur.execute(""" CREATE TABLE IF NOT EXISTS Questions(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    quest_number INTEGER NOT NULL,
                                    quest_text TEXT UNIQUE NOT NULL ,
                                    is_deleted BOOLEAN DEFAULT FALSE
                                )
            """)

            self.cur.execute("""CREATE TABLE IF NOT EXISTS Answers(
                                    id SERIAL PRIMARY KEY NOT NULL,
                                    question_number INTEGER ,
                                    user_id BIGINT,
                                    choice INT,
                                    hashsum CHARACTER VARYING(50) UNIQUE 
                                )""")

    def add_user(self, user_id, user_name, message_date):
        with self.conn:
            self.cur.execute(f"SELECT id FROM Users WHERE id_tg={user_id}")
            id_data = self.cur.fetchone()
            if id_data is None:
                date_login = datetime.fromtimestamp(message_date).strftime('%d-%m-%y %H:%M:%S')
                self.cur.execute("INSERT INTO Users(id_tg, username, date_reg) VALUES(%s,%s,%s);",
                                 (user_id, user_name, date_login))
                self.conn.commit()

    def add_init_questions(self):
        values = [[i+1, value] for i, value in enumerate(QUESTIONS)]
        self.cur.executemany(""" INSERT INTO questions(quest_number, quest_text) VALUES(%s, %s) 
                                    ON CONFLICT(quest_text) DO NOTHING """, values)
        self.conn.commit()

    def update_user_data(self, cols: list, values: list, id_tg: int):

        self.cur.execute(
            sql.SQL("""UPDATE Users SET {cols} = {values} WHERE "id_tg" = %s """).format(
                        cols=sql.SQL(',').join([sql.Identifier(col) for col in cols]),
                        values=sql.SQL(',').join([sql.Literal(value) for value in values])
            ), (id_tg,)
        )
        self.conn.commit()

    def get_user_data(self, cols: list, id_tg: str):
        self.cur.execute(
            sql.SQL('SELECT {cols} FROM Users WHERE "id_tg" = %s ').format(
                        cols=sql.SQL(',').join([sql.Identifier(col) for col in cols])
            ), (id_tg,)
        )
        return self.cur.fetchone()[0]

    def del_user(self, user_id):
        with self.conn:
            self.cur.execute("DELETE FROM Users WHERE id_tg = %s;", (user_id,))
            self.conn.commit()

    def get_question_text(self, quest_number):
        with self.conn:
            self.cur.execute("SELECT quest_text FROM questions WHERE quest_number = %s", (quest_number, ))
            return self.cur.fetchone()[0]

    def get_result_by_school(self):
        with self.conn:
            self.cur.execute("SELECT school, question_number, AVG(choice) FROM answers, users "
                             "WHERE answers.user_id = users.id_tg "
                             "GROUP BY school, question_number ORDER BY school, question_number")
            return self.cur.fetchall()

    def get_result_by_region(self):
        with self.conn:
            self.cur.execute("SELECT region, question_number, AVG(choice) FROM answers, users "
                             "WHERE answers.user_id = users.id_tg "
                             "GROUP BY region, question_number ORDER BY region, question_number")
            return self.cur.fetchall()

    def get_all_results(self):
        with self.conn:
            self.cur.execute("SELECT question_number, AVG(choice) FROM answers GROUP BY question_number "
                             "ORDER BY question_number")
            return self.cur.fetchall()

    def add_user_choice(self, question_number, user_id, choice, hashsum):
        with self.conn:
            self.cur.execute("INSERT INTO answers(question_number, user_id,choice, hashsum) VALUES(%s, %s, %s, %s) "
                             "ON CONFLICT(hashsum) DO UPDATE SET choice = excluded.choice",
                             (question_number, user_id, choice, hashsum))

    def get_all_questions(self):
        with self.conn:
            self.cur.execute("SELECT quest_number, quest_text FROM questions")
            return self.cur.fetchall()

    # def add_answer

    # def add_user_contact(self, user_id, user_phone):
    #     with self.conn:
    #         self.cur.execute("UPDATE Users SET phone_numb = %s WHERE id_tg =%s;", (user_phone, user_id,))
    #         self.conn.commit()
    #
    # def get_user_temp(self, user_id):
    #     with self.conn:
    #         self.cur.execute("SELECT temp FROM users_information WHERE user_id = "
    #                          "(SELECT id FROM users WHERE id_tg = %s)", (user_id, ))
    #         return self.cur.fetchone()[0]
    #
    # def set_user_temp(self, user_id, temp):
    #     with self.conn:
    #         self.cur.execute("UPDATE users_information SET temp = %s WHERE user_id = "
    #                          "(SELECT id FROM users WHERE id_tg = %s)", (temp, user_id,))
    #         self.conn.commit()