import os
import re

from tweepy import API
from tweepy import OAuthHandler
from tweepy import StreamListener, Stream

import credentials as cred
import json


class MyStreamListener(StreamListener):
    tweets = []

    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.tweets = []

    def on_error(self, status_code):
        if status_code == 420:
            return False

    def on_data(self, raw_data):
        data = json.loads(raw_data)
        if 'created_at' in data:
            text_to_append = ""
            if 'retweeted_status' in data:
                if 'extended_tweet' in data['retweeted_status']:
                    text_to_append = data['retweeted_status']['extended_tweet']['full_text']
                else:
                    text_to_append = data['retweeted_status']['text']
            else:
                if 'extended_tweet' in data:
                    text_to_append = data['extended_tweet']['full_text']
                else:
                    text_to_append = data['text']
            self.tweets.append(text_to_append)

    def save(self):
        with open(self.filename, 'w') as file:
            json.dump(self.tweets, file)


class MyStreamer:

    def __init__(self, listener):
        auth = OAuthHandler(cred.CONSUMER_KEY, cred.CONSUMER_SECRET)
        auth.set_access_token(cred.ACCESS_TOKEN, cred.ACCESS_SECRET)
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True)
        self.listener = listener
        self.stream = Stream(auth=api.auth, listener=listener)

    def sample_tweets(self):
        self.stream.sample(languages=['en'], is_async=True)

    def filter_tweets(self, track):
        self.stream.filter(languages=['en'], is_async=True, track=track)


def get_tweets(refresh=False, num_tweets=2000, clean=True, track=None):
    """

    :param refresh:
    :param num_tweets:
    :param clean:
    :return:
    :param track:
    """
    tweets = []
    if not os.path.exists('data/tweets.json'):
        refresh = True
    if refresh:
        sys_listener = MyStreamListener("data/tweets.json")
        sys_stream = MyStreamer(sys_listener)
        if filter is None:
            sys_stream.sample_tweets()
        else:
            sys_stream.filter_tweets(track)

        while True:
            if len(sys_listener.tweets) >= num_tweets:
                sys_stream.stream.disconnect()
                tweets = sys_listener.tweets
                sys_listener.save()
                break
    else:
        with open('data/tweets.json', 'r') as file:
            tweets = json.load(file)

    if clean:
        if isinstance(tweets, list):
            tweets = " ".join(tweets)
    return tweets


if __name__ == "__main__":
    get_tweets()
