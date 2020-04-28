from .twitter_config import TwitterConfig
from .mongo_config import MongoConfig
from .bot_config import BotConfig
from json import load
from os import environ


class Configs:

    def __init__(self):
        settings_file = environ.get('SETTINGS_FILE', 'settings.json')
        with open(f'src/configs/{settings_file}', 'r') as raw_data:
            raw_data = load(raw_data)
            self.twitter_config = TwitterConfig(raw_data['twitter'])
            self.mongo_config = MongoConfig(raw_data['mongo'])
            self.bot_config = BotConfig(raw_data['bot'])
