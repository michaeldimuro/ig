import os
from InstagramAPI import InstagramAPI
import time
import datetime
from random import randint
from examples.db import DB



class Bot:

    api = None
    db = DB()
    username = ''
    interests = []
    tags = ['business', 'marketing', 'seo', 'webdesign', 'entrepreneur']
    myFollowers = []
    botFollowed = []
    unfollow = False

    def __init__(self, username, password, copy):
        self.username = username
        self.api = InstagramAPI(username, password)
        if self.api.login():
            if not os.path.exists('accounts/' + username):
                os.mkdir('accounts/' + username)
            self.writeLog("Successful Login!")
            self.db.create_connection("accounts/" + username + "/data.db")
            self.resolveCopyAccounts(copy)
            self.run()
        else:
            self.writeLog("Could not log in to this account.")

    def resolveCopyAccounts(self, c):
        for i in range(0, len(c) - 1):
            self.api.searchUsername(c[i])
            self.interests.append(self.api.LastJson['user']['pk'])

    def run(self):

        if len(self.botFollowed) == 0:
            self.botFollowed = self.db.bot_followed(self.username)

        self.myFollowers = self.api.getTotalSelfFollowers()

        #likes = 0
        while True:

            # Follow Based on Interest
            if self.unfollow == False:
                self.writeLog("Getting interest followers..")
                interestFollowers = self.api.getTotalFollowers(self.interests[randint(0, len(self.interests) - 1)])
                randFollowStart = randint(0, len(interestFollowers) - 1)
                currentFollowIndex = randFollowStart

            for i in range(1, randint(27, 35)):
                if self.unfollow == False:
                    if currentFollowIndex + 1 == len(interestFollowers):
                        currentFollowIndex = 0
                    targetFollow = interestFollowers[currentFollowIndex]
                    if self.api.follow(targetFollow['pk']) == False:
                        break
                    self.botFollowed.append(targetFollow['pk'])
                    self.db.add_follow(self.username, targetFollow['pk'])
                    self.writeLog("Followed user: " + str(targetFollow['username']))
                    currentFollowIndex = currentFollowIndex + 1
                    time.sleep(randint(1, 3))
                else:
                    self.writeLog("Unfollowing some users..")
                    targetUnfollow = self.botFollowed[len(self.botFollowed) - 1]
                    if self.api.unfollow(targetUnfollow) == False:
                        break
                    self.db.remove_followed(self.username, targetUnfollow)
                    self.botFollowed.pop()
                    if len(self.botFollowed) == 0:
                        self.unfollow = False


            if self.unfollow == False and len(self.botFollowed) >= 500:
                self.botFollowed.reverse()
                self.unfollow = True

            sleepTime = randint(1200, 1450)
            sleepTimeInMins = sleepTime/60
            self.writeLog("Taking a break for " + str(sleepTimeInMins) + " minutes.")
            time.sleep(sleepTime)

    def writeLog(self, line):
        if self.username != '':
            try:
                file = open('accounts/' + self.username + '/log.txt', 'r')
            except IOError:
                file = open('accounts/' + self.username + '/log.txt', 'w')

            file.close()
            f = open('accounts/' + self.username + '/log.txt', 'a')
            currentDT = datetime.datetime.now()
            f.write(str(currentDT) + ': ' + line + "\n")
            f.close()

    def getPID(self):
        return os.getpid()


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