from InstagramAPI import InstagramAPI
import time
from random import randint


class Bot:

    api = InstagramAPI()

    def __init__(self, username, password):
        api = InstagramAPI(username, password)
        if api.login():
            run()
        else:
            print("Could not start bot for account %s", username)

    def run(self):

    api = InstagramAPI("michaeldimuro", "beastmedia123")

    interests = [30442728]
    tags = ['business', 'marketing', 'seo', 'webdesign', 'entrepreneur']
    myFollowers = []
    botFollowed = []
    unfollow = False

    if api.login():
        myFollowers = api.getTotalSelfFollowers()
        # interestFollowers = api.getTotalFollowers(interests[0])

        likes = 0
        while True:

            # Follow Based on Interest
            print("Getting interest followers")
            if unfollow == False:
                interestFollowers = api.getTotalFollowers(interests[randint(0, len(interests) - 1)])
                randFollowStart = randint(0, len(interestFollowers) - 1)
                currentFollowIndex = randFollowStart

            for i in range(1, randint(14, 23)):
                if unfollow == False:
                    if currentFollowIndex + 1 == len(interestFollowers):
                        break
                    targetFollow = interestFollowers[currentFollowIndex]
                    if api.follow(targetFollow['pk']) == False:
                        break
                    botFollowed.append(targetFollow['pk'])
                    print("Followed user: " + str(targetFollow['username']))
                    currentFollowIndex = currentFollowIndex + 1
                    time.sleep(randint(1, 3))
                else:
                    print("Unfollowing some users..")
                    targetUnfollow = botFollowed[len(botFollowed) - 1]
                    if api.unfollow(targetUnfollow) == False:
                        break
                    botFollowed.pop()
                    if len(botFollowed) == 0:
                        unfollow = False


            if unfollow == False and len(botFollowed) >= 500:
                botFollowed.reverse()
                unfollow = True

            print("Taking a break..")
            time.sleep(randint(1200, 1450))


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