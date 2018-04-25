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
    bedTime = datetime.now()
    wakeupTime = datetime.now()

    def __init__(self, username, password, copy):
        self.username = username
        self.api = InstagramAPI(username, password)
        if self.api.login():
            if not os.path.exists('accounts/' + username):
                os.mkdir('accounts/' + username)
            self.writeLog("Successful Login!")
            self.db = DB("accounts/" + username + "/data.db")
            self.botFollowed = self.db.bot_followed(self.username)
            time.sleep(randint(4, 32))
            self.copyAccounts = copy
            self.resolveCopyAccounts(copy)
            self.setSleepClock()
        else:
            print("\nCould not log in to " + self.username + "\n")
            exit()

    def resolveCopyAccounts(self, c):
        for i in range(0, len(c)):
            self.api.searchUsername(c[i])
            try:
                copyAccountID = self.api.LastJson['user']['pk']
                self.writeLog("Found Copy Account: " + str(c[i]))
                self.interests.append(copyAccountID)
                time.sleep(randint(6, 42))
            except:
                self.writeLog("Invalid Copy Account: " + str(c[i]))
                time.sleep(randint(17, 42))
                pass

    def setSleepClock(self):
        now = datetime.now()

        bedTimeHour = randint(1, 3)
        bedTimeMinute = randint(0, 59)
        self.bedTime = now.replace(day=int(now.day) + 1,hour=bedTimeHour, minute=bedTimeMinute, second=randint(0, 59))

        wakeupTimeHour = randint(6, 8)
        wakeupTimeMinute = randint(0, 59)
        self.wakeupTime = now.replace(hour=int(wakeupTimeHour) + 1, minute=wakeupTimeMinute, second=randint(0, 59))

    def run(self):

        # SET INITIAL FOLLOW VARIABLE
        unfollow = False
        forceUnfollow = False
        # FETCH EXPIRATION TIME
        expires = datetime.strptime(self.db.expired(), "%Y-%m-%d %H:%M:%S.%f")

        followUpperBound = randint(490, 562)
        followLowerBound = randint(224, 298)

        # IF BOTFOLLOW IS EMPTY, TRY TO FETCH FROM DATABASE
        if len(self.botFollowed) == 0:
            self.botFollowed = self.db.bot_followed(self.username)
            # VERIFY RELATIONSHIPS IN CASE USER MANUALLY UNFOLLOWED DURING DOWNTIME
            self.checkRelationships()

        # FINISHED SETTING UP


        # MAIN APPLICATION LOOP
        while True:

            copyFollowers = []

            if len(self.interests) == 0:
                self.writeLog("No users left in interests pool.")
                exit()
            # CHECK FOR SUBSCRIPTION EXPIRATION - IF EXPIRED, START UNFOLLOWING AND

            now = datetime.now()

            if expires <= now:
                self.writeLog("Subscription has expired. Unfollowing all users and cleaning up..")
                forceUnfollow = True

            if self.bedTime <= now and now <= self.wakeupTime:
                self.writeLog("ANTIBAN: Humans need to sleep too.. Waking up at " + str(self.wakeupTime.time().hour))
                time.sleep(randint(3000, 3600))
                pass


            if forceUnfollow and len(self.botFollowed) == 0:
                self.writeLog("Finished Cleaning Up.. Shutting down.")
                exit()

            if not unfollow and not forceUnfollow:
                copyUserIndex = randint(0, len(self.interests) - 1)
                self.writeLog("Getting Copy Followers from " + str(self.copyAccounts[copyUserIndex]))
                copyFollowers = self.api.getTotalFollowers(self.interests[copyUserIndex])

            actionRange = randint(11, 35)
            for i in range(1, actionRange):

                # IF PREVIOUS DATABASE LIST IS GREATER THAN 500 USERS, SET TO START UNFOLLOWING
                if len(self.botFollowed) >= followUpperBound:
                    self.botFollowed.reverse()
                    unfollow = True
                    self.writeLog("Following more than " + str(followUpperBound) + " users. Switched to unfollow.")
                    followUpperBound = randint(490, 562)

                if len(self.botFollowed) <= followLowerBound and unfollow and not forceUnfollow:
                    self.botFollowed.reverse()
                    unfollow = False
                    self.writeLog("Following less than " + str(followLowerBound) + " users. Switched to follow.")
                    followLowerBound = randint(224, 298)

                if not unfollow and not forceUnfollow and len(copyFollowers) != 0:
                    randomFollowIndex = randint(0, len(copyFollowers) - 1)
                    if randomFollowIndex == len(copyFollowers) - 1:
                        randomFollowIndex = 0
                    targetFollow = copyFollowers[randomFollowIndex]
                    if randint(0, 100) > 50 and targetFollow['is_private'] == False:
                        self.api.getUserFeed(str(targetFollow['pk']))
                        s = randint(3, 15)
                        self.writeLog(
                            "ANTIBAN: Fetching feed for: " + str(targetFollow['username']) + ".. sleeping for " + str(s) + " seconds.")
                        time.sleep(s)
                        if randint(0, 100) >= 30:
                            randomFollowerFeed = self.api.LastJson['items']
                            if len(randomFollowerFeed) > 0:
                                for i in range(1, randint(0, 5)):
                                    mediaId = randomFollowerFeed[randint(0, len(randomFollowerFeed) - 1)]['id']
                                    self.api.mediaInfo(mediaId)
                                    time.sleep(randint(1, 3))
                                    self.api.like(mediaId)
                                    self.writeLog("Liked " + targetFollow['username'] + " photo")
                                    time.sleep(randint(3, 7))
                    if targetFollow['pk'] in self.botFollowed:
                        self.writeLog("Already following " + str(targetFollow['pk']) + ".. skipping over.")
                        pass
                    if not self.api.follow(targetFollow['pk']):
                        self.writeLog("Could not follow anymore users right now..")
                        break
                    else:
                        self.botFollowed.append(targetFollow['pk'])
                        self.db.add_follow(self.username, targetFollow['pk'])
                        s = randint(1, 9)
                        self.writeLog("ANTIBAN: Followed user: " + str(targetFollow['username'] + " sleeping for " + str(s) + " seconds.."))
                        time.sleep(s)
                        # if targetFollow['pk'] in self.interests:
                        #     self.interests.remove(targetFollow['pk'])

                else:
                    if len(self.botFollowed) > 0:
                        self.writeLog("Unfollowing some users..")
                        targetUnfollow = self.botFollowed[len(self.botFollowed) - 1]
                        if not self.api.unfollow(targetUnfollow):
                            break
                        self.db.remove_followed(self.username, targetUnfollow)
                        self.botFollowed.pop()
                        time.sleep(randint(4, 12))
                    else:
                        break

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
        sleepTime = randint(900, 1440)
        sleepTimeInMins = sleepTime / 60
        sleepTimeExtraSecs = sleepTime % 60
        self.writeLog(
            "ANTIBAN: Taking a break for " + str(sleepTimeInMins) + " minutes " + str(sleepTimeExtraSecs) + " seconds.")
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