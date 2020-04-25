from .twitter_config import TwitterConfig
from .mongo_config import MongoConfig
from json import load


class Configs:

    def __init__(self):
        with open('src/configs/settings.json', 'r') as raw_data:
            raw_data = load(raw_data)
            self.twitter_config = TwitterConfig(raw_data['twitter'])
            self.mongo_config = MongoConfig(raw_data['mongo'])
