class TwitterConfig:

    def __init__(self, raw_data):
        self.access_token = raw_data['access_token']
        self.access_token_secret = raw_data['access_token_secret']
        self.api_key = raw_data['api_key']
        self.api_secret_key = raw_data['api_secret_key']
