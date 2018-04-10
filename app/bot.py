import os
from InstagramAPI import InstagramAPI
import time
from datetime import datetime
from pytz import timezone
from random import randint
from db import DB

class Bot:

    api = None
    db = None
    username = ''
    interests = []
    botFollowed = []
    copyAccounts = []

    def __init__(self, username, password, copy):
        self.username = username
        self.api = InstagramAPI(username, password)
        if self.api.login():
            if not os.path.exists('accounts/' + username):
                os.mkdir('accounts/' + username)
            self.writeLog("Successful Login!")
            self.db = DB("accounts/" + username + "/data.db")
            self.botFollowed = self.db.bot_followed(self.username)
            self.copyAccounts = copy
            self.resolveCopyAccounts(copy)
        else:
            print("\nCould not log in to " + self.username + "\n")
            exit()

    def resolveCopyAccounts(self, c):
        for i in range(0, len(c)):
            self.api.searchUsername(c[i])
            try:
                copyAccountID = self.api.LastJson['user']['pk']
                self.writeLog("Getting interest followers from " + str(c[i]))
                copyFollowers = self.api.getTotalFollowers(copyAccountID)

                if len(copyFollowers) >= 15000:
                    self.writeLog("Caching 15000 users from " + str(c[i]))
                    randFollowStart = randint(0, len(copyFollowers) - 15001)
                    self.interests = self.interests + copyFollowers[randFollowStart:randFollowStart + 15000]
                else:
                    self.writeLog("Caching " + str(len(copyFollowers)) + " users from " + str(c[i]))
                    self.interests = self.interests + copyFollowers
            except:
                self.writeLog("Invalid Copy Account: " + str(c[i]))
                pass



    def run(self):

        # SET INITIAL FOLLOW VARIABLE
        unfollow = False
        forceUnfollow = False
        # FETCH EXPIRATION TIME
        expires = datetime.strptime(self.db.expired(), "%Y-%m-%d %H:%M:%S.%f")

        # IF BOTFOLLOW IS EMPTY, TRY TO FETCH FROM DATABASE
        if len(self.botFollowed) == 0:
            self.botFollowed = self.db.bot_followed(self.username)
            # VERIFY RELATIONSHIPS IN CASE USER MANUALLY UNFOLLOWED DURING DOWNTIME
            self.checkRelationships()

        # FINISHED SETTING UP


        # MAIN APPLICATION LOOP
        while True:

            if len(self.interests) == 0:
                self.writeLog("No users left in interests pool.")
                exit()
            # CHECK FOR SUBSCRIPTION EXPIRATION - IF EXPIRED, START UNFOLLOWING AND
            if expires <= datetime.now():
                self.writeLog("Subscription has expired. Unfollowing all users and cleaning up..")
                forceUnfollow = True

            if forceUnfollow and len(self.botFollowed) == 0:
                self.writeLog("Finished Cleaning Up.. Shutting down.")
                exit()

            # IF PREVIOUS DATABASE LIST IS GREATER THAN 500 USERS, SET TO START UNFOLLOWING
            if len(self.botFollowed) >= 500:
                self.botFollowed.reverse()
                unfollow = True

            # # GATHER LIST OF USERS TO FOLLOW FROM A COPY ACCOUNT
            # if not unfollow and not forceUnfollow:
            #     randomCopyIndex = randint(0, len(self.interests) - 1)
            #     self.writeLog("Getting interest followers from " + str(self.copyAccounts[randomCopyIndex]))
            #     interestFollowers = self.api.getTotalFollowers(self.interests[randomCopyIndex])
            #     randFollowStart = randint(0, len(interestFollowers) - 1)
            #     currentFollowIndex = randFollowStart
            #     self.writeLog("Finished retrieving interest followers")

            for i in range(1, randint(27, 35)):
                if not unfollow and not forceUnfollow:
                    randomFollowIndex = randint(0, len(self.interests))
                    if randomFollowIndex == len(self.interests):
                        randomFollowIndex = 0
                    targetFollow = self.interests[randomFollowIndex]
                    if targetFollow['pk'] in self.botFollowed:
                        self.writeLog("Already following " + str(targetFollow['pk']) + ".. skipping over.")
                        pass
                    if not self.api.follow(targetFollow['pk']):
                        self.writeLog("Could not follow anymore users right now..")
                        break
                    else:
                        self.botFollowed.append(targetFollow['pk'])
                        self.db.add_follow(self.username, targetFollow['pk'])
                        self.writeLog("Followed user: " + str(targetFollow['username']))
                        if targetFollow['pk'] in self.interests:
                            self.interests.remove(targetFollow['pk'])
                        time.sleep(randint(1, 3))
                else:
                    if len(self.botFollowed) > 0:
                        self.writeLog("Unfollowing some users..")
                        targetUnfollow = self.botFollowed[len(self.botFollowed) - 1]
                        if not self.api.unfollow(targetUnfollow):
                            self.checkRelationships()
                            break
                        self.db.remove_followed(self.username, targetUnfollow)
                        self.botFollowed.pop()
                        if len(self.botFollowed) <= 250 and not forceUnfollow:
                            self.botFollowed.reverse()
                            self.unfollow = False
                        time.sleep(randint(1, 3))

            self.writeLog("Current Amount of Tracked Following: " + str(len(self.botFollowed)))
            self.randomBreak()

    def checkRelationships(self):
        self.writeLog("Checking relationships..")
        following = self.api.getTotalSelfFollowings()
        for i in range(0, len(self.botFollowed)):
            if self.botFollowed[i] not in following:
                self.db.remove_followed(str(self.username), str(self.botFollowed[i]))

        self.botFollowed = self.db.bot_followed(self.username)

    def randomBreak(self):
        sleepTime = randint(1080, 1440)
        sleepTimeInMins = sleepTime / 60
        sleepTimeExtraSecs = sleepTime % 60
        self.writeLog(
            "Taking a break for " + str(sleepTimeInMins) + " minutes " + str(sleepTimeExtraSecs) + " seconds.")
        time.sleep(sleepTime)

    def writeLog(self, line):
        if self.username != '':
            try:
                file = open('accounts/' + self.username + '/log.txt', 'r')
            except IOError:
                file = open('accounts/' + self.username + '/log.txt', 'w')

            file.close()
            f = open('accounts/' + self.username + '/log.txt', 'a')
            fmt = '%d-%m-%Y %H:%M:%S'
            eastern = timezone('US/Eastern')
            loc_dt = datetime.now(eastern)
            currentDT = loc_dt.strftime(fmt)
            f.write(str(currentDT) + ': ' + line + "\n")
            f.close()


            # # FIND A RANDOM FOLLOWER
            # randomFollower = myFollowers[randint(0, len(myFollowers) - 1)]
            #
            # # LIKE RANDOM PICTURES
            # if randint(0, 100) < 70:
            #     if randomFollower['is_private'] == False:
            #         _ = api.getUserFeed(randomFollower['pk'])
            #         randomFollowerFeed = api.LastJson['items']
            #         if len(randomFollowerFeed) > 0:
            #             for i in range(1, randint(1, 4)):
            #                 mediaId = randomFollowerFeed[randint(0, len(randomFollowerFeed) - 1)]['id']
            #                 api.like(mediaId)
            #                 print("Liked " + randomFollower['username'] + " photo")
            #                 time.sleep(randint(4, 9))
            #
            #         time.sleep(randint(6, 10))
            #
            #     # if likes >= 10:
            #     # 	break
            #
            # # FOLLOW FOLLOWERS FOLLOWERS
            # if randint(0, 100) >= 70:
            #     if unfollow == False:
            #         if randomFollower['is_private'] == False:
            #             randomFollowersFollowers = api.getTotalFollowers(randomFollower['pk'])
            #             randomFollowersFollower = randomFollowersFollowers[randint(0, len(randomFollowersFollowers) - 1)]
            #             api.follow(randomFollowersFollower['pk'])
            #             botFollowed.append(randomFollowersFollower['pk'])
            #             print("Followed: " + randomFollowersFollower['username'])
            #             if len(botFollowed) >= 500:
            #                 unfollow = True
            #             time.sleep(randint(3, 15))
            #     else:
            #         print("Unfollowing: " + str(botFollowed[0]))
            #         api.unfollow(botFollowed[len(botFollowed) - 1])
            #         botFollowed.remove(0)
            #         if len(botFollowed) == 0:
            #             unfollow = False
            #
            # if randint(0, 1000) < 10:
            #     naptime = randint(2520, 5400)
            #     print("Sleeping for " + str(naptime) + " seconds..")
            #     time.sleep(naptime)