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

# How to run

To start a streaming client I recommend to use supervisor. Place this config to `/etc/supervisor/conf.d/streaming.conf`

```
[program:twitter_streaming]
command=/usr/bin/python /home/ubuntu/sweepy/stream.py
directory=/home/ubuntu/sweepy
autostart=true
autorestart=true
startretries=3
stderr_logfile=/home/ubuntu/stream.err.log
stdout_logfile=/home/ubuntu/stream.out.log
user=ubuntu
```

Change the configuration according to your enviroment. I put this script on EC2

Reread the configuration

```
sudo supervisorctl reread
```

And update the configuration

```
sudo supervisorctl update
```

The script should be up and running. 

# Processer script

You can just run 

```
make run-processer
```

It will process the raw tweet and create a users collection and make the tweet as `processed`
