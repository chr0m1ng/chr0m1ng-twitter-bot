from facades import MarkovChainFacade
from constants.twitter.tweet import MAX_LENGTH

mcf = MarkovChainFacade()

chains = mcf.create_chain()

while True:
    print(mcf.generate_phrase(chains, MAX_LENGTH))
    input('press anything to create another tweet...')
