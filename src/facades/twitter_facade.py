from services import MongoService, TwitterService
from constants.mongo.collections import BOT_TWEETS_COLLECTION, TWEETS_COLLECTION
from progress.spinner import PieSpinner


class TwitterFacade:

    def __init__(self):
        self.mongo_service = MongoService()
        self.twitter_service = TwitterService()

    def save_tweets(self, tweets, is_bot_tweet=False):
        return self.__save(tweets, self.__save_tweets, is_bot_tweet)

    def save_tweet(self, tweet, is_bot_tweet=False):
        return self.__save(tweet, self.__save_tweet, is_bot_tweet)

    def __save(self, data, save_method, is_bot_tweet=False):
        client = self.mongo_service.connect()
        save_method(client, data, is_bot_tweet)
        client.close()

    def __save_tweets(self, client, tweets, is_bot_tweet=False):
        return self.__save_mongo(client, tweets, self.mongo_service.force_save_many_data, is_bot_tweet)

    def __save_tweet(self, client, tweet, is_bot_tweet=False):
        return self.__save_mongo(client, tweet, self.mongo_service.force_save_data, is_bot_tweet)

    def __save_mongo(self, client, data, save_method, is_bot_tweet=False):
        collection = TWEETS_COLLECTION if is_bot_tweet is False else BOT_TWEETS_COLLECTION
        success = save_method(
            data,
            collection,
            client
        )
        return success

    def get_saved_tweets(self):
        client = self.mongo_service.connect()
        tweets = self.mongo_service.force_get_data(TWEETS_COLLECTION, client)
        client.close()

        return tweets

    def harvest_my_tweets_json(self):
        for tweet in PieSpinner('Harvesting tweets and saving...').iter(self.harvest_my_tweets()):
            yield tweet._json

    def harvest_my_tweets(self):
        max_id = None
        tweets = []
        while len(tweets) > 0 or max_id is None:
            tweets = self.twitter_service.get_user_timeline(
                user_id=self.twitter_service.get_my_id(),
                count=200,
                include_rts=False,
                max_id=max_id
            )
            for tweet in tweets:
                yield tweet
            if len(tweets) > 0:
                max_id = tweets[-1].id
            else:
                max_id = -1
