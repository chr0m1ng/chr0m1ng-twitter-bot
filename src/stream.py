from facades import TwitterFacade
from listeners import TweetListener
from services import TwitterService

tf = TwitterFacade()
tl = TweetListener()

tf.setup_my_stream(tl)
