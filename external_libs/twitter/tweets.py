import sys
import os
import json
import tweepy
from textblob import TextBlob


sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app.producer import producer

consumer_key = 'your_consumer_key'
consumer_secret = 'your_consumer_secret'
access_token = 'your_access_token'
access_secret = 'your_access_secret'

# Authenticate to Twitter
# auth = tweepy.OAuth2AppHandler(
#     os.getenv('TWITTER_API_KEY'),
#     os.getenv('TWITTER_API_SECRET')
# )
auth = tweepy.OAuth2AppHandler('YSrAdlSHklt0KjLX7jvjq1rqc', 'bitvWNwy9BxzuTmtdbel9DuhUczJdxPidBptQu1rsUKNnz5f52')
# Create API object
api = tweepy.API(auth)


class MyStreamListener(tweepy.StreamListener):
    def __init__(self, producer):
        self.producer = producer
        super().__init__()

    # on success
    def on_data(self, data):

        # decode json
        dict_data = json.loads(data)

        # pass tweet into TextBlob
        tweet = TextBlob(dict_data["text"])

        # output sentiment polarity
        print(tweet.sentiment.polarity)

        # determine if sentiment is positive, negative, or neutral
        if tweet.sentiment.polarity < 0:
            sentiment = "negative"
        elif tweet.sentiment.polarity == 0:
            sentiment = "neutral"
        else:
            sentiment = "positive"

        # output sentiment
        print(sentiment)

    def on_status(self, status):
        # Send the tweet text to Kafka
        print(status.text)
        self.producer.send('election', status.text.encode('utf-8'))


if __name__ == '__main__':
    # Start streaming tweets and sending them to Kafka
    myStreamListener = MyStreamListener(producer)
    print('here ooooo')
    myStream = tweepy.Stream(auth=api.auth, listener=myStreamListener)
    myStream.filter(track=['asiwaju', 'BAT', 'tinubu'])
