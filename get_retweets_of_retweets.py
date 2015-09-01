#!/usr/bin/env python
import pymongo
import tweepy

from pymongo import MongoClient

from sweepy.get_config import get_config

config = get_config()

consumer_key = config.get('PROCESS_TWITTER_CONSUMER_KEY')
consumer_secret = config.get('PROCESS_TWITTER_CONSUMER_SECRET')
access_token = config.get('PROCESS_TWITTER_ACCESS_TOKEN')
access_token_secret = config.get('PROCESS_TWITTER_ACCESS_TOKEN_SECRET')

MONGO_URL = config.get('MONGO_URL')
MONGO_PORT = config.get('MONGO_PORT')
MONGO_USERNAME = config.get('MONGO_USERNAME')
MONGO_PASSWORD = config.get('MONGO_PASSWORD')

client = MongoClient(MONGO_URL, int(MONGO_PORT))

print 'Establishing Tweepy connection'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3)

db = client.tweets
db.authenticate(MONGO_USERNAME, MONGO_PASSWORD)

raw_tweets = db.raw_tweets

if __name__ == "__main__":
    tweets = []
    for doc in raw_tweets.find({'retweeted_status.id_str' : '636345902915911680'}):
        tweets.append(doc)

    print 'Fetch {} documents'.format(len(tweets))
    for tweet in tweets:
        try:
            print 'Processing {}'.format(tweet['id_str'])
            retweets = api.retweets(tweet['id_str'], count=100)
            if retweets:
                print retweets 
        except tweepy.error.TweepError:
            pass




