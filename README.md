# Sweepy
Sweepy is a twitter client to capture twitter activities and store in MongoDB for any media analysis. The script is two parts, `stream.py` is a client to listen to a particular keyword or twitter user and capture the activity to MongoDB. `sweepy.py` is a script to get all the followers and friends and save it to MongoDB. Currently, the script only gets id because getting all the user details is not practical due to Twitter rate limit.

# What you need
You need to create `.env` file and fill in as shown below
```
MONGO_URL=
MONGO_PORT=
MONGO_USERNAME=
MONGO_PASSWORD=

STREAM_TWITTER_CONSUMER_KEY=
STREAM_TWITTER_CONSUMER_SECRET=
STREAM_TWITTER_ACCESS_TOKEN=
STREAM_TWITTER_ACCESS_TOKEN_SECRET=

PROCESS_TWITTER_CONSUMER_KEY=
PROCESS_TWITTER_CONSUMER_SECRET=
PROCESS_TWITTER_ACCESS_TOKEN=
PROCESS_TWITTER_ACCESS_TOKEN_SECRET=

```

You also need a running MongoDB

#Install dependencies
Run 

```
pip install -r requirements.txt
```


