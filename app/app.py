import os
import multiprocessing
from datetime import datetime
from bot import Bot
from db import DB

def startBot(username, password, copy):
    b = Bot(username, password, copy)
    b.run()

if __name__ == "__main__":

    db = DB()
    jobs = []

    while True:
        print("\nSelect an Option:\n"
              "1. List Active Accounts\n"
              "2: Add User\n"
              "3: Pause User\n"
              "4: Remove User\n"
              "5: Exit\n")

        inp = raw_input("Selection: ")

        if inp == '1':
            if len(jobs) == 0:
                print("\n\nNo accounts have been added.")
            else:
                print("\n\nActive Accounts:")
                for i in range(0, len(jobs)):
                    currentJob = jobs[i]
                    status = ""
                    if currentJob[1].is_alive():
                        db.create_connection("accounts/" + currentJob[0] + "/data.db")
                        expires = db.expired()
                        status = "ACTIVE (Expires " + str(expires) + ")"
                    else:
                        if os.path.exists('accounts/' + currentJob[0]):
                            db.create_connection("accounts/" + currentJob[0] + "/data.db")
                            expires = datetime.strptime(db.expired(), "%Y-%m-%d %H:%M:%S.%f")
                            if expires >= datetime.now():
                                status = "DEAD"
                            else:
                                status = "DEAD | NOT EXPIRED - RELOAD ACCOUNT"
                    print(str(i + 1) + ": " + currentJob[0] + " - " + status)

            print("\n")
        elif inp == '2':
            copy = []
            username = raw_input("Username: ")
            password = raw_input("Password: ")

            for i in range(0, 3):
               a = raw_input("Copy " + str(i + 1) + ": ")
               copy.append(a)

            p = multiprocessing.Process(target=startBot, args=(username, password, copy,))
            jobs.append([username, p])
            p.start()

        elif inp == '3':
            print("T")
        elif inp == '4':
            userToTerminate = raw_input("User To Remove: ")
            userToTerminate = int(userToTerminate) - 1
            if userToTerminate > len(jobs):
                print("Invalid Selection")
            else:
                user = jobs[userToTerminate][0]
                jobToTerminate = jobs[userToTerminate][1]
                jobToTerminate.terminate()
                jobs.remove(jobs[userToTerminate])
                print("\n" + user + ": Account has been removed.\n")
        elif inp == '5':
            confirmation = raw_input("Are you sure you want to exit? All accounts will be shut down (Y/N): ")
            if confirmation == 'y' or confirmation == 'Y':
                exit()
            elif confirmation == 'n' or confirmation == 'N':
                continue
            else:
                print("\nInvalid option\n")


