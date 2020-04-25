from configs import Configs
import twitter


class TwitterService:

    def __init__(self):
        twitter_config = Configs().twitter_config
        access_token = twitter_config.access_token
        access_token_secret = twitter_config.access_token_secret
        api_key = twitter_config.api_key
        api_secret_key = twitter_config.api_secret_key

        self.client = twitter.Api(
            consumer_key=api_key,
            consumer_secret=api_secret_key,
            access_token_key=access_token,
            access_token_secret=access_token_secret
        )

    def get_my_id(self):
        creds = self.client.VerifyCredentials()
        return creds.id

    def get_user_timeline(
            self, user_id=None, screen_name=None,
            since_id=None, max_id=None, count=None,
            include_rts=True, trim_user=False, exclude_replies=False
    ):
        return self.client.GetUserTimeline(
            user_id, screen_name, since_id,
            max_id, count, include_rts,
            trim_user, exclude_replies
        )

    def list_my_tweets(self):
        tweets = self.client.GetUserTimeline(
            user_id=self.get_my_id(),
            count=200,
            exclude_replies=True,
            include_rts=False
        )

        while len(tweets) > 0:
            for tweet in tweets:
                yield tweet
            tweets = self.client.GetUserTimeline(
                user_id=self.get_my_id(),
                count=200,
                include_rts=False,
                max_id=tweets[-1].id
            )
