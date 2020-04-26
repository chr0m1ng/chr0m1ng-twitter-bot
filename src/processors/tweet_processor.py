from constants.twitter.tweet import FULL_TEXT_KEY, BOT_WOEID

RT_PREFIX = 'RT'


class TweetProcessor:

    @staticmethod
    def clean_tweet_text(tweet):
        # will do something to remove accentuation, links and etc
        return tweet.text

    @staticmethod
    def get_tweet_words(tweet):
        cleaned_tweet = TweetProcessor.clean_tweet_text(tweet)
        return cleaned_tweet.split(' ')

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
