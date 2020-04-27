from constants.markov_chains.word_types import *
from constants.markov_chains.keys import *
from processors import TweetProcessor
from facades import TwitterFacade
from services import MongoService
from progress.bar import ShadyBar
from functools import reduce
from random import choice, choices

N_DIGITS_ROUND = 2
CHAINS_COLLECTION = 'chains'


class MarkovChainFacade:

    def __init__(self):
        self.twitter_facade = TwitterFacade()
        self.mongo_service = MongoService()

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

    def save_chain(self, markov_chain):
        client = self.mongo_service.connect()
        self.mongo_service.force_save_data(
            markov_chain, CHAINS_COLLECTION, client
        )
        client.close()

    def choose_next_word(self, nodes):
        words = []
        rates = []
        for w, v in nodes.items():
            words.append(w)
            rates.append(v[R_OCCURR_KEY])
        if len(words) == 0:
            print('eitaaa')
        [next_word] = choices(words, rates)
        return next_word

    def decide_word_type(self, w_type_node):
        [word_type] = choices(
            [MID_WORD, END_WORD],
            [w_type_node[R_MID_KEY], w_type_node[R_END_KEY]]
        )
        return word_type

    def generate_phrase(self, markov_chain, max_len):
        initial_word = choice(
            [w for w, v in markov_chain.items() if v[IS_INIT_KEY]]
        )
        phrase = initial_word
        current_nodes = markov_chain[initial_word][NODES_KEY]
        next_word_type = MID_WORD
        while next_word_type != END_WORD and len(phrase) <= max_len and len(current_nodes) > 0:
            next_word = self.choose_next_word(current_nodes)
            phrase += f' {next_word}'
            next_word_type = self.decide_word_type(
                current_nodes[next_word][W_TYPE_KEY]
            )
            current_nodes = markov_chain[next_word][NODES_KEY]
        if len(phrase) > max_len:
            phrase = phrase[:max_len - 1]
        return TweetProcessor.decode_tweet(phrase)
