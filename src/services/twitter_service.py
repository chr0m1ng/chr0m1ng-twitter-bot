from configs import Configs
import tweepy


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

    def get_my_id(self):
        creds = self.client.me()
        return creds.id

    def get_my_timeline(self, max_id=None, count=None, include_rts=False):
        return self.client.user_timeline(
            max_id=max_id, count=count, include_rts=include_rts,
            user_id=self.get_my_id(), tweet_mode='extended'
        )
