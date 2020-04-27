from facades import MarkovChainFacade
from json import dumps

mcf = MarkovChainFacade()

chain = mcf.create_chain()
mcf.save_chain(chain)
