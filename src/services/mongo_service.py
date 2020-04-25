from configs import Configs
from pymongo.errors import ConnectionFailure
from pymongo import MongoClient


class MongoService:

    def __init__(self):
        mongo_config = Configs().mongo_config
        self.connection_string = mongo_config.connection_string
        self.database = mongo_config.database

    def connect(self):
        try:
            client = MongoClient(self.connection_string)
            client.test
            return client
        except ConnectionFailure:
            return None

    def get_collection(self, collection_name, client):
        db_connection = client[self.database]
        return db_connection[collection_name]

    def force_save_many_data(self, many_data, collection_name, client):
        return self.__force_save(many_data, collection_name, self.save_many_data, client)

    def force_save_data(self, data, collection_name, client):
        return self.__force_save(data, collection_name, self.save_data, client)

    def save_data(self, data, collection_name, client):
        try:
            collection = self.get_collection(collection_name, client)
            collection.insert(data)
            return True
        except Exception as ex:
            print(ex)
            return False

    def save_many_data(self, many_data, collection_name, client):
        try:
            collection = self.get_collection(collection_name, client)
            collection.insert_many(many_data)
            return True
        except Exception as ex:
            print(ex)
            return False

    def __force_save(self, data, collection_name, save_method, client):
        max_attempts = 10
        attempt = 0
        success = save_method(data, collection_name, client)

        while success is False and attempt < max_attempts:
            success = save_method(
                data,
                collection_name,
                client
            )
            attempt += 1

        if success is False:
            print(f'Failed to save {data}')

        return success

    def get_data(self, collection_name, client):
        try:
            collection = self.get_collection(collection_name, client)
            return list(collection.find())
        except:
            return list()

    def force_get_data(self, collection_name, client):
        max_attempts = 10
        attempt = 0
        data = self.get_data(collection_name, client)

        while len(data) == 0 and attempt < max_attempts:
            data = self.get_data(collection_name, client)
            attempt += 1

        if len(data) == 0:
            print(f'Failed to get data from {collection_name}')

        return data
