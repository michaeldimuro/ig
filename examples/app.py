import os
import multiprocessing
import datetime
import time
from bot import Bot


accounts = []

def startBot(i, copy):
    _ = Bot(accounts[len(accounts) - 1][0], accounts[len(accounts) - 1][1], copy)

if __name__ == "__main__":

    jobs = []

    while True:
        print("Select an Option:\n"
              "1. List Active Accounts\n"
              "2: Add User\n"
              "3: Pause User\n"
              "4: Remove User\n")

        inp = raw_input("Selection: ")

        if inp == '1':
            if len(accounts) == 0:
                print("\n\nNo accounts have been added.")
            else:
                print("\n\nActive Accounts:")
                for i in range(0, len(accounts)):
                    print(accounts[i][0])
            print("\n")
        elif inp == '2':
            copy = []
            username = raw_input("Username: ")
            password = raw_input("Password: ")
            user = [username, password]
            accounts.append(user)
            for i in range(0, 3):
                a = raw_input("Copy " + str(i + 1) + ": ")
                copy.append(a)

            p = multiprocessing.Process(target=startBot, args=(len(accounts), copy))
            jobs.append(p)
            p.start()

        elif inp == '3':
            print("Three")


