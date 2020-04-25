from facades import TwitterFacade
from json import dumps

tf = TwitterFacade()

my_tweets = tf.harvest_my_tweets_json()

tf.save_tweets(my_tweets)
