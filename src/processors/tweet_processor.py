from constants.twitter.tweet import FULL_TEXT_KEY, BOT_WOEID
from string import punctuation

RT_PREFIX = 'RT'
EMPTY_SPACE = ' '


class TweetProcessor:

    @staticmethod
    def is_only_punctuation(word):
        return all(char in punctuation for char in word)

    @staticmethod
    def clean_tweet(tweet_json):
        words = TweetProcessor.get_tweet_words(tweet_json[FULL_TEXT_KEY])
        return [
            w.lower() for w in words
            if TweetProcessor.is_only_punctuation(w) is False
        ]

    @staticmethod
    def get_tweet_words(tweet_text):
        return tweet_text.split(EMPTY_SPACE)

    @staticmethod
    def process_stream_tweet(tweet):
        tweet_json = tweet._json
        tweet_json[FULL_TEXT_KEY] = tweet.text
        return tweet_json

    @staticmethod
    def is_retweet(tweet):
        return tweet.text.startswith(RT_PREFIX)

    @staticmethod
    def is_bot_tweet(tweet):
        return tweet.place.id == BOT_WOEID if tweet.place is not None else False
