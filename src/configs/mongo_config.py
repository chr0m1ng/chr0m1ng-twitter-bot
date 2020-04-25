class MongoConfig:

    def __init__(self, raw_data):
        self.connection_string = raw_data['connection_string']
        self.database = raw_data['database']
