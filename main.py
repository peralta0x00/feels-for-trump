from __future__ import division 
import json, re, time, schedule, time, datetime 
from textblob import TextBlob
import threading
from threading import Thread

makeTweet = __import__('tweet out')
tweetStream = __import__('get tweets')

negativeCount = 0
positiveCount = 0
aboutRussia = 0
global fileName
tweets = []
fileName = "/Users/kevperalta/Desktop/python/twitter/data.txt"

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
                break
            counter += 1
        if (trumpLoc and notLoc) != 0 and trumpLoc < notLoc:
            if trumpLoc > notLoc - 2:
                return True
            
def getTweets():
    temp = []
    global fileName
    with open(fileName, "r") as dataFile:
        for line in dataFile:
            i = line.decode('utf-8', 'ignore')
            temp.append(i.lower() + "\n")

    if temp is not None:
        open(fileName, 'w')
        return temp
    else:
        print("loading tweets still...")
        

def addToCounter(value, revert):
    global negativeCount
    global positiveCount
    if revert:
        value = value * -1
    if value < 0:
        negativeCount += 1
    else:
        positiveCount += 1

def tweetOut(p, n, percentage):
    perc = round(percentage, 2)
    makeTweet.tweetPrettily(positiveCount, negativeCount, perc)

def main():
    global negativeCount, positiveCount, aboutRussia, tweets
    tweets = getTweets()
    aboutRussia = negativeCount = positiveCount = 0
    if len(tweets) > 0:
        print("number of tweets: " + str(len(tweets)))        
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
        print("tweeted!")
        tweetOut(positiveCount, negativeCount, (aboutRussia/len(tweets))*100)
    else:
        print("not enough tweets")
def thread1():
    print("start")
    while True: #will just keep on going
        print("ran main")
        main()
        time.sleep(1800)
        
def thread2():
    Thread(target = thread1).start()
    tweetStream.startStream()
        
thread2()

    
