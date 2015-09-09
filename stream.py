#!/usr/bin/env python
#Import the necessary methods from tweepy library
from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
import json
from pymongo import MongoClient

from sweepy.get_config import get_config

config = get_config()

MONGO_URL = config.get('MONGO_URL')
MONGO_PORT = config.get('MONGO_PORT')
MONGO_USERNAME = config.get('MONGO_USERNAME')
MONGO_PASSWORD = config.get('MONGO_PASSWORD')
MONGO_DATABASE = config.get('MONGO_DATABASE')

connection = MongoClient(MONGO_URL, int(MONGO_PORT))
db = connection[MONGO_DATABASE]

  # MongoLab has authentication
db.authenticate(MONGO_USERNAME, MONGO_PASSWORD)

#Variables that contains the user credentials to access Twitter API
consumer_key = config.get('STREAM_TWITTER_CONSUMER_KEY')
consumer_secret = config.get('STREAM_TWITTER_CONSUMER_SECRET')
access_token = config.get('STREAM_TWITTER_ACCESS_TOKEN')
access_token_secret = config.get('STREAM_TWITTER_ACCESS_TOKEN_SECRET')

#This is a basic listener that just prints received tweets to stdout.
class StdOutListener(StreamListener):

    def on_data(self, data):
        mydata = json.loads(data)
        db.raw_tweets.insert_one(mydata)
        return True

    def on_error(self, status):
        mydata = json.loads(status)
        db.error_tweets.insert_one(mydata)


if __name__ == '__main__':

    #This handles Twitter authetification and the connection to Twitter Streaming API
    l = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    stream = Stream(auth, l)

    #This line filter Twitter Streams to capture data by the keywords: 'python', 'javascript', 'ruby'
    stream.filter(follow=['121817564'])
