from facades import MarkovChainFacade
from json import dumps

mcf = MarkovChainFacade()

chain = mcf.create_chain()
print(dumps(chain, indent=4))
