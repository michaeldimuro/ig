import os
import signal
import multiprocessing
from multiprocessing import Manager
import datetime
import time
from bot import Bot
from db import DB

def startBot(username, password, copy):
    b = Bot(username, password, copy)
    b.run()

if __name__ == "__main__":

    jobs = []

    p = multiprocessing.Process(target=startBot, args=("blitzmediamarketing", "mikedimuro99", ["icomeup", "icomeup", "icomeup"]))
    jobs.append(["blitzmediamarketing", p])
    p.start()

    p = multiprocessing.Process(target=startBot, args=("ijerseywebdesign", "mikedimuro99", ["icomeup", "icomeup", "icomeup"]))
    jobs.append(["ijerseywebdesign", p])
    p.start()

    print(jobs)

    while True:
        print("Select an Option:\n"
              "1. List Active Accounts\n"
              "2: Add User\n"
              "3: Pause User\n"
              "4: Remove User\n"
              "5: Exit")

        inp = raw_input("Selection: ")

        if inp == '1':
            if len(jobs) == 0:
                print("\n\nNo accounts have been added.")
            else:
                print("\n\nActive Accounts:")
                for i in range(0, len(jobs)):
                    print(str(i + 1) + ": " + jobs[i][0])

            print("\n")
        elif inp == '2':
            copy = []
            username = raw_input("Username: ")
            password = raw_input("Password: ")
            user = [username, password]

            for i in range(0, 3):
               a = raw_input("Copy " + str(i + 1) + ": ")
               copy.append(a)

            p = multiprocessing.Process(target=startBot, args=(username, password, copy,))
            jobs.append([username, p])
            p.start()

        elif inp == '3':
            print("Three")
        elif inp == '4':
            userToTerminate = raw_input("User To Remove: ")
            userToTerminate = int(userToTerminate) - 1
            if userToTerminate > len(jobs):
                print("Invalid Selection")
            else:
                jobToTerminate = jobs[userToTerminate][1]
                jobToTerminate.terminate()
                jobs.remove(jobs[userToTerminate])
                print("Account has been removed.")
        elif inp == '5':
            exit()


