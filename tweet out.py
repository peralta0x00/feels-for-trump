import tweepy
gettweets = __import__('get tweets')
config = gettweets.config

auth = tweepy.OAuthHandler(config[0], config[1])
auth.set_access_token(config[2], config[3])
api = tweepy.API(auth)

def tweet(string):
    api.update_status(string)


def tweetPrettily(positiveTweets, negativeTweets, percentage):
    string = "Negatively charged tweets: " + str(positiveTweets) + "\nPositively charged tweets: " + str(negativeTweets)
    string = string + "\nPercentage of tweets about Russia: " + percentage
    api.update_status(string)

