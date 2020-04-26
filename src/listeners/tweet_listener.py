from tweepy import StreamListener
from processors import TweetProcessor
from facades import TwitterFacade


class TweetListener(StreamListener):

    def on_status(self, tweet):
        if TweetProcessor.is_retweet(tweet):
            print(f'Discarding retweet "{tweet.text}"')
            return
        tweet_json = TweetProcessor.process_stream_tweet(tweet)
        is_bot_tweet = TweetProcessor.is_bot_tweet(tweet)
        tf = TwitterFacade()
        tf.save_tweet(tweet_json, is_bot_tweet)

    def on_error(self, status_code):
        print(f'err with status code: {status_code}')
        return True
