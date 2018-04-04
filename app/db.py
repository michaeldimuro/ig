import sqlite3
import datetime
from sqlite3 import Error

class DB:

    conn = None

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.text_factory = str
            self.create_tables()
        except Error as e:
            print(e)

    def add_follow(self, user, followed):
        self.conn.execute("INSERT INTO followed (user, followed) VALUES (?, ?)", (user, followed))
        self.conn.commit()

    def remove_followed(self, user, followed):
        self.conn.execute("DELETE FROM followed WHERE user=? AND followed=?", (user, followed))


    def bot_followed(self, user):
        followed = []
        cur = self.conn.cursor()
        followedQuery = cur.execute("SELECT followed FROM followed WHERE user=?", (user,))
        rows = followedQuery.fetchall()
        for row in rows:
            followed.append(str(row[0]))

        return followed

    def set_prefs(self):
        self.conn.execute("INSERT OR REPLACE INTO prefs (activated, expires) VALUES (?, ?)", (datetime.datetime.now(), datetime.datetime.now() + datetime.timedelta(days=30)))
        self.conn.commit()

    def expired(self):
        cur = self.conn.cursor()
        expiredQuery = cur.execute("SELECT * FROM prefs")
        row = expiredQuery.fetchone()
        result = row[1]
        return result



    def create_tables(self):
        self.conn.execute('''CREATE TABLE if not exists prefs (activated datetime, expires datetime, setting int DEFAULT 0)''')
        self.conn.commit()
        self.set_prefs()
        # self.conn.execute('''CREATE TABLE if not exists copy (user text, followed text)''')
        # self.conn.commit()
        self.conn.execute('''CREATE TABLE if not exists followed (user text, followed text)''')
        self.conn.commit()

    def close(self):
        self.conn.close()