class TweetProcessor:

    @staticmethod
    def clean_tweet_text(tweet):
        # will do something to remove accentuation, links and etc
        return tweet.text

    @staticmethod
    def get_tweet_words(tweet):
        cleaned_tweet = TweetProcessor.clean_tweet_text(tweet)
        return cleaned_tweet.split(' ')
