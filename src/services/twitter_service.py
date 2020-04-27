from configs import Configs
import tweepy

TWEET_MODE_EXTENDED = 'extended'


class TwitterService:

    def __init__(self):
        twitter_config = Configs().twitter_config
        access_token = twitter_config.access_token
        access_token_secret = twitter_config.access_token_secret
        api_key = twitter_config.api_key
        api_secret_key = twitter_config.api_secret_key

        auth = tweepy.OAuthHandler(api_key, api_secret_key)
        auth.set_access_token(access_token, access_token_secret)

        self.client = tweepy.API(auth, wait_on_rate_limit=True)

    def get_my_id_str(self):
        creds = self.client.me()
        return creds.id_str

    def get_my_id(self):
        creds = self.client.me()
        return creds.id

    def get_my_timeline(self, max_id=None, count=None, include_rts=False):
        return self.client.user_timeline(
            max_id=max_id, count=count, include_rts=include_rts,
            user_id=self.get_my_id(), tweet_mode=TWEET_MODE_EXTENDED
        )

    def get_my_stream(self, stream_listener):
        return self.get_stream(stream_listener, [self.get_my_id_str()])

    def get_stream(self, stream_listener, twitters):
        tweet_stream = tweepy.Stream(self.client.auth, stream_listener)
        tweet_stream.filter(follow=twitters, is_async=True)
        return tweet_stream

    def post_tweet(self, tweet, place_id=None):
        return self.client.update_status(status=tweet, place_id=place_id)
