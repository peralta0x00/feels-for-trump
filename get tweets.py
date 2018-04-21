import tweepy
import json
import time
import threading
import turtle
from tweepy import Stream 
from queue import *
from threading import Thread

from textblob import TextBlob
from tweepy.streaming import StreamListener

global config, stream #tweetQueue
tweetQueue = Queue()
config = ["---", "----", "---", "---"] 
auth = tweepy.OAuthHandler(config[0], config[1])
auth.set_access_token(config[2], config[3])
api = tweepy.API(auth)

class Listener(StreamListener): #main tweeet stream; keeps adding to queue to be processed
    global tweetQueue
    def on_data(self, data):
        try:
            json_load = json.loads(data)
            text = json_load['text']
            coded = text.encode('utf-8')
            tmp = coded.decode('utf-8', 'ignore')
            tweetQueue.put(tmp)
        except KeyError:
            pass
    def on_error(self, status):
        print(status)
        print("error")

def getTweetsThread(): #setting up and initiating tweet stream

    listener = Listener()
    stream = Stream(auth, listener)
    try:
        stream.filter(track = ['Trump', 'trump', "Trump's","trump's", "Donald Trump", "President", 'president','make america great again', '#maga'], stall_warnings=True)
    except Exception:
        pass

class tweetObject(object):
    def __init__(self, tweet):
        self.text = tweet.lower()
        russianInvolvement = False
    def printout(self):
        print(self.text)    
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

def process(tweets):
    info = [0,0,0] #positive, negative, about russia
    while tweets.empty() is False:
        tweet = tweetObject(tweets.get())
        sentiment = tweet.sentimentValue()
        if tweet.aboutRussia():
            info[2] +=1
        if sentiment != 0:
            if tweet.revertSentiment():
                sentiment *= -1
            if sentiment < 0:
                info[0] += 1
            else:
                info[1] += 1
    return info
            
def tweetOut(neg, pos, russia):
    perc = round((russia/float(neg+pos)*100), 3)
    string = "Negatively charged tweets: " + str(pos) + "\nPositively charged tweets: " + str(neg)
    string = string + "\nPercentage of tweets about Russia: " + str(perc) + "%"
    api.update_status(string)
    print("tweeted")


def main(): #thread 1
    global tweetQueue
    print("started up...\n")
    while True:
        time.sleep(1800) #let other thread collect items
        sentimentVals = process(tweetQueue)
        tweetOut(sentimentVals[0], sentimentVals[1], sentimentVals[2])

Thread(target = main).start()
getTweetsThread()
Thread(target = Listener).start()        



        

    


