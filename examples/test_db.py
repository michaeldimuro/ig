from examples import DB

if __name__ == '__main__':
    db = DB()
    db.create_connection("data.db")
    print(db.bot_followed("blitzmediamarketing"))
