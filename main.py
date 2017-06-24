from __future__ import division 
import json, re, time, schedule, time 
from textblob import TextBlob
makeTweet = __import__('tweet out')

negativeCount = 0
positiveCount = 0
aboutRussia = 0
tweets = []

class tweetObject(object):
    def __init__(self, tweet):
        self.text = tweet.lower()
        russianInvolvement = False
    def printout(self):
        print self.text    
    def sentimentValue(self):
        blob = TextBlob(self.text)
        if self.text.find("fake news") != -1:
            return 1
        return blob.sentiment.polarity
    def aboutRussia(self):
        if self.text.find("putin") != -1 or self.text.find("russia") != -1 or self.text.find("vladimir") != -1 or self.text.find("collusion") != -1:
            return True
        return False
    def revertSentiment(self):
        words = []
        trumpLoc = notLoc = counter = 0
        foundIs = False
        for i in self.text.split(" "):
            i = i.lower()
            if i == "trump" or i == "trump's":
                trumpLoc = counter
            if (i == "not" or i == "isn't" or i == "isnt") and trumpLoc != 0:
                notLoc = counter
            counter += 1
        if (trumpLoc and notLoc) != 0 and trumpLoc < notLoc:
            if trumpLoc > notLoc - 2:
                return True
            
def getTweets(fileName):
    temp = []
    tweetFile = open(fileName, "r+")
    tweetFile.flush()
    for i in tweetFile:
        if i.decode('utf-8', 'ignore') not in temp:
            i = i.decode('utf-8', 'ignore')
            temp.append(i.lower() + "\n")
    return temp

def addToCounter(value, revert):
    global negativeCount
    global positiveCount
    if revert:
        value = value * -1
    if value < 0:
        negativeCount += 1
    else:
        positiveCount += 1


def main():
    fileLocation = "/Users/kevperalta/Desktop/python/twitter/data.txt"
    global negativeCount, positiveCount, aboutRussia, tweets
    tweets = getTweets(fileLocation)
    aboutRussia = negativeCount = positiveCount = 0
    if len(tweets) != 0:
        for i in tweets:
            tweet = tweetObject(i)
            sentiment = tweet.sentimentValue()
            if sentiment != 0:
                if tweet.revertSentiment():
                    addToCounter(sentiment, True)
                else:
                    addToCounter(sentiment, False)
            if tweet.aboutRussia():
                aboutRussia += 1

        makeTweet.tweetPrettily(positiveCount, negativeCount, str( int(aboutRussia/len(tweets)* 100) /100))
main()
schedule.every(5).minutes.do(main) 
while True:
    schedule.run_pending()
    time.sleep(5)

