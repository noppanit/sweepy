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

# How to deploy

I've decided to use Docker to deploy the application. As Docker is the latest and gretest so why not. The process is a little bit strange but why not!. This application can be deployed to any docker machine.

After you've spun up a new machine with Docker running. If you're using Amazon EC2 please have a look at this [page](http://docs.aws.amazon.com/AmazonECS/latest/developerguide/docker-basics.html), in case you want to install Docker on Amazon AMI.

## Build your image

```
make build-docker
```

## Run the container
```
make run-container
```

# Run streaming client
You can just run 

```
make run-stream
```

# Run processer client
```
make run-processer
```

It will process the raw tweet and create a users collection and make the tweet as `processed`
