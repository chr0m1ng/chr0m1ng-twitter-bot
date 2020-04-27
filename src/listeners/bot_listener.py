from configs import Configs
from tweepy import StreamListener
from processors import TweetProcessor
from constants.twitter.tweet import MAX_LENGTH
from facades import TwitterFacade, MarkovChainFacade


class BotListener(StreamListener):

    def should_process(self, tweet):
        bot_config = Configs().bot_config
        return tweet.user.id_str in bot_config.follow_triggers and tweet.in_reply_to_user_id is None

    def on_status(self, tweet):
        try:
            if self.should_process(tweet) is False:
                print(f'Discarding tweet "{tweet.text}"')
                return
            tf = TwitterFacade()
            mcf = MarkovChainFacade()
            chains = mcf.create_chain()
            bot_tweet = mcf.generate_phrase(chains, MAX_LENGTH)
            print(bot_tweet)
            post = tf.post_bot_tweet(bot_tweet)
            mcf.save_chain(chains)
            tf.save_tweet(post._json, True)
        except Exception as ex:
            print(ex)

    def on_error(self, status_code):
        print(f'err with status code: {status_code}')
        return True
