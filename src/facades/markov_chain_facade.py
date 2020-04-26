from constants.markov_chains.keys import *
from processors import TweetProcessor
from facades import TwitterFacade
from progress.bar import ShadyBar
from functools import reduce

N_DIGITS_ROUND = 2


class MarkovChainFacade:

    def __init__(self):
        self.twitter_facade = TwitterFacade()

    def get_clean_tweets(self):
        tweets = self.twitter_facade.get_saved_tweets()
        return [TweetProcessor.clean_tweet(t) for t in tweets]

    def get_total_occurrences(self, mkc_word):
        return reduce(
            lambda x, y: x + y,
            [
                w[N_OCCURR_KEY]
                for w in mkc_word[NODES_KEY].values()
            ],
            0
        )

    def get_total_chain_nodes(self, markov_chain):
        return reduce(
            lambda x, y: x + y,
            [len(w[NODES_KEY]) for w in markov_chain.values()]
        )

    def calculate_rates(self, markov_chain):
        bar = ShadyBar(
            'Calculating chain rates',
            max=self.get_total_chain_nodes(markov_chain)
        )
        for word in markov_chain:
            total_occurr = self.get_total_occurrences(markov_chain[word])
            for node in markov_chain[word][NODES_KEY]:
                n_occurr = markov_chain[word][NODES_KEY][node][N_OCCURR_KEY]
                n_mid = markov_chain[word][NODES_KEY][node][W_TYPE_KEY][N_MID_KEY]
                n_end = markov_chain[word][NODES_KEY][node][W_TYPE_KEY][N_END_KEY]
                markov_chain[word][NODES_KEY][node][R_OCCURR_KEY] = round(
                    n_occurr / total_occurr, N_DIGITS_ROUND
                )
                markov_chain[word][NODES_KEY][node][W_TYPE_KEY][R_MID_KEY] = round(
                    n_mid / n_occurr, N_DIGITS_ROUND
                )
                markov_chain[word][NODES_KEY][node][W_TYPE_KEY][R_END_KEY] = round(
                    n_end / n_occurr, N_DIGITS_ROUND
                )
                bar.next()
        bar.finish()
        return markov_chain

    def get_total_tweets_words(self, tweets):
        return reduce(lambda x, y: x + y, [len(t) for t in tweets])

    def create_chain(self):
        tweets = self.get_clean_tweets()
        markov_chain = {}
        bar = ShadyBar(
            'Populating chain',
            max=self.get_total_tweets_words(tweets)
        )
        for tweet in tweets:
            for index, word in enumerate(tweet):
                if word not in markov_chain:
                    markov_chain[word] = {
                        NODES_KEY: {},
                        IS_INIT_KEY: False
                    }
                if markov_chain[word][IS_INIT_KEY] is False:
                    markov_chain[word][IS_INIT_KEY] = index == 0
                if index != len(tweet) - 1:
                    following_word = tweet[index + 1]
                    if following_word not in markov_chain[word][NODES_KEY]:
                        markov_chain[word][NODES_KEY][following_word] = {
                            N_OCCURR_KEY: 0,
                            W_TYPE_KEY: {
                                N_END_KEY: 0,
                                N_MID_KEY: 0
                            }
                        }
                    markov_chain[word][NODES_KEY][following_word][N_OCCURR_KEY] += 1
                    w_type_n = N_END_KEY
                    if index + 1 != len(tweet) - 1:
                        w_type_n = N_MID_KEY
                    markov_chain[word][NODES_KEY][following_word][W_TYPE_KEY][w_type_n] += 1
                bar.next()
        bar.finish()
        return self.calculate_rates(markov_chain)
