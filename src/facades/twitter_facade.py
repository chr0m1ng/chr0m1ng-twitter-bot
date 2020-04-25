from services import MongoService

TWEET_COLLECTION = 'tweets'
BOT_TWEET_COLLECTION = 'bot_tweets'


class TwitterFacade:

    def __init__(self):
        self.mongo_service = MongoService()

    def save_tweet(self, tweet, is_bot_tweet=False):
        collection = TWEET_COLLECTION if is_bot_tweet is False else BOT_TWEET_COLLECTION
        client = self.mongo_service.connect()
        success = self.mongo_service.force_save_data(
            tweet,
            collection,
            client
        )
        client.close()

        return success

    def get_tweets(self):
        client = self.mongo_service.connect()
        tweets = self.mongo_service.force_get_data(TWEET_COLLECTION, client)
        client.close()

        return tweets
