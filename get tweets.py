import tweepy
import json
import time
from urllib3.exceptions import ProtocolError

global config, dataFile, stream
canRun = True
config = ["---", "---", "---", "---"] 
dataFile = open("/Users/kevperalta/Desktop/python/twitter/data.txt", "w")
from tweepy import Stream
from tweepy.streaming import StreamListener
class Listener(StreamListener):
    def on_data(self, data):
        try:
            json_load = json.loads(data)
            text = json_load['text']
            coded = text.encode('utf-8')
            dataFile.write(coded + "\n")
        except KeyError:
            pass
    def on_error(self, status):
        print(status)
        print("error")

def startStream():
    global stream
    auth = tweepy.OAuthHandler(config[0], config[1])
    auth.set_access_token(config[2], config[3])
    api = tweepy.API(auth)
    listener = Listener()
    stream = Stream(auth, listener)
    print("looking")
    try:
        stream.filter(track = ["trump", "trumps", "trump's"], stall_warnings=True)
    except ProtocolError:
        print(ProtocolError)
        pass
