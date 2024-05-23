import sqlite3
from pathlib import Path


class Database:
    def __init__(self):
        '''Инициализация соединения с БД'''
        # .db, .db3, .sqlite, .sqlite3
        self.connection = sqlite3.connect(Path(__file__).parent.parent / 'db.sqlite3')
        self.cursor = self.connection.cursor()

    def create_tables(self):

        '''Создание таблиц'''
        self.cursor.execute('DROP TABLE IF EXISTS anketa')
        self.cursor.execute('DROP TABLE IF EXISTS likes')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS anketa (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tg_id INTEGER,
                nickname TEXT,
                age INTEGER,
                gender TEXT,
                extra_text TEXT,
                photo TEXT,
                UNIQUE (tg_id)
            )
        ''')
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS likes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                liker INTEGER,
                owner INTEGER,
                status INTEGER,
                UNIQUE (liker,owner)
            )
        ''')

        self.connection.commit()

    def insert_anketa(self, data: dict):
        self.cursor.execute('''
            INSERT INTO anketa (tg_id, nickname, age, gender, extra_text, photo) 
            VALUES (:tg_id, :nickname, :age, :gender, :extra_text, :photo);
            ''',
                {
                    'tg_id' : data['tg_id'],
                    'nickname': data['nickname'],
                    'age': data['age'],
                    'gender': data['gender'],
                    'extra_text': data['extra_text'],
                    'photo' : data['photo']
                }
                        )
        self.connection.commit()

    def is_exists(self, int_tg_id):
        self.cursor.execute('''
        SELECT * FROM anketa WHERE tg_id = :int_tg_id
        ''', {'int_tg_id': int_tg_id})
        return self.cursor.fetchone()

    def select_ankets(self, tg_id):
        self.cursor.execute('''
        SELECT * FROM anketa WHERE tg_id NOT IN(
        SELECT likes.owner FROM likes
        WHERE liker = :tg_idd
        AND likes.status IS NOT NULL)
        AND anketa.tg_id != :tg_idd
        ''', {'tg_idd':tg_id})
        return self.cursor.fetchall()

    def insert_like(self, liker, owner, status):
        self.cursor.execute('''
        INSERT INTO likes(liker, owner, status)
        VALUES (:liker, :owner, :status)
        ''', {'liker':liker,
                'owner': owner,
                'status':status})
        self.connection.commit()




if __name__ == '__main__':
    db = Database()
    db.create_tables()
