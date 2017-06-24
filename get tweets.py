import tweepy
import json
from urllib3.exceptions import ProtocolError

global config
config = ["QRdK2RbgffkecWnE6ocakekoQ", "9onYOS4aTXCSFFt5kn7dPKdZK3RU764V8krT7ZqUp8pDgX0oNB", "878488031128190977-AJm7Pn1zBhAI5UrR0MpWEenalPp9i94", "9OUsvHC3YBBoSktgTuHW8ZZtKdFLAn0KkMzhfInedq7KN"]
    
from tweepy import Stream
from tweepy.streaming import StreamListener
class Listener(StreamListener):
    def on_data(self, data):
        try:
            json_load = json.loads(data)
            text = json_load['text']
            coded = text.encode('utf-8')
            s = str(coded)
            print(s)
        except KeyError:
            pass
    def on_error(self, status):
        print(status)
        print("error")


if __name__ == '__main__':
    auth = tweepy.OAuthHandler(config[0], config[1])
    auth.set_access_token(config[2], config[3])
    api = tweepy.API(auth)
    listener = Listener()
    stream = Stream(auth, listener)
    try:
        stream.filter(track = ["trump", "trumps", "trump's"], stall_warnings=True)
    except ProtocolError:
        pass
