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

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=3)

db = client.tweets
db.authenticate(MONGO_USERNAME, MONGO_PASSWORD)

raw_tweets = db.raw_tweets
users = db.users

def is_user_in_db(user_id):
    return get_user_from_db(user_id) is None

def get_user_from_db(user_id):
    return users.find_one({'user.id' : user_id})

def get_user_from_twitter(user_id):
    return api.get_user(user_id)

def get_followers(user_id):
    users = []
    for i, page in enumerate(tweepy.Cursor(api.followers, id=user_id, count=200).pages()):
        print 'Getting page {} for followers'.format(i)
        users += page
    return users

def get_friends(user_id):
    users = []
    for i, page in enumerate(tweepy.Cursor(api.friends, id=user_id, count=200).pages()):
        print 'Getting page {} for friends'.format(i)
        users += page
    return users

def get_followers_ids(user_id):
    ids = []
    for i, page in enumerate(tweepy.Cursor(api.followers_ids, id=user_id, count=5000).pages()):
        print 'Getting page {} for followers ids'.format(i)
        ids += page

    return ids

def get_friends_ids(user_id):
    ids = []
    for i, page in enumerate(tweepy.Cursor(api.friends_ids, id=user_id, count=5000).pages()):
        print 'Getting page {} for friends ids'.format(i)
        ids += page
    return ids

def process_user(user):
    user_id = user['id']
    screen_name = user['screen_name']
    
    print 'Processing user : {}'.format(screen_name)

    the_user = get_user_from_db(user_id)
    if the_user is None:
        user['followers_ids'] = get_followers_ids(screen_name)
        user['friends_ids'] = get_friends_ids(screen_name)

        users.insert_one(user)

if __name__ == "__main__":

    for doc in raw_tweets.find({'processed' : {'$exists': False}}):
        print 'Start processing'
        try:
            process_user(doc['user'])
        except KeyError:
            pass

        try:
            process_user(doc['retweeted_status']['user'])
        except KeyError:
            pass

        raw_tweets.update_one({'_id': doc['_id']}, {'$set':{'processed':True}})
