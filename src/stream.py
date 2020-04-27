from facades import TwitterFacade
from listeners import TweetListener
from services import TwitterService

while True:
    try:
        tf = TwitterFacade()
        tl = TweetListener()

        tf.setup_my_stream(tl)
        input('Running stream...')
