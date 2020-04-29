from listeners import BotListener
from facades import TwitterFacade
from configs import Configs

tf = TwitterFacade()
bot_listener = BotListener()
bot_configs = Configs().bot_config

tf.setup_tweet_stream(bot_listener, bot_configs.follow_triggers)
