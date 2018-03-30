import sqlite3
from sqlite3 import Error

class DB:

    conn = None

    def create_connection(self, db_file):
        """ create a database connection to a SQLite database """
        try:
            self.conn = sqlite3.connect(db_file)
            self.conn.text_factory = str
            self.create_tables()
            print(sqlite3.version)
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
        followedQuery = cur.execute("SELECT followed FROM followed WHERE user=? ORDER BY followed DESC", (user,))
        rows = followedQuery.fetchall()
        for row in rows:
            followed.append(str(row[0]))

        return followed


    def create_tables(self):
        self.conn.execute('''CREATE TABLE if not exists followed (user text, followed text)''')
        self.conn.commit()