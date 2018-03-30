import os
import multiprocessing
from multiprocessing import Manager
import datetime
import time
from bot import Bot
from db import DB

# bots = []

def startBot(username, password, copy, botsList):
    # pid.append(os.getpid())
    b = Bot(username, password, copy)
    botsList.append(b)

if __name__ == "__main__":

    manager = multiprocessing.Manager()
    bots = manager.list()

    jobs = []
    db = DB()
    db.create_connection("data.db")

    while True:
        print("Select an Option:\n"
              "1. List Active Accounts\n"
              "2: Add User\n"
              "3: Pause User\n"
              "4: Remove User\n"
              "5: Exit")

        inp = raw_input("Selection: ")

        if inp == '1':
            if len(bots) == 0:
                print("\n\nNo accounts have been added.")
            else:
                print("\n\nActive Accounts:")
                for i in range(0, len(bots)):
                    print(str(i) + ": " + bots[i].username + " - PID: " + bots[i].getPID())

            print("\n")
        elif inp == '2':
            copy = []
            username = raw_input("Username: ")
            password = raw_input("Password: ")
            user = [username, password]

            for i in range(0, 3):
               a = raw_input("Copy " + str(i + 1) + ": ")
               copy.append(a)

            p = multiprocessing.Process(target=startBot, args=(username, password, copy, bots))
            jobs.append(p)
            p.start()

        elif inp == '3':
            print("Three")
        elif inp == '5':
            exit()


