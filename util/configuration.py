import json


class Configuration:
    def __init__(self):
        self.binance_api_key = ''
        self.binance_api_secret = ''
        self.mongo_uri = ''
        self.read()

    def write(self):
        with open('data.json','w') as file:
            json.dump(self.to_list(), file)

    def read(self):
        with open('data.json','r') as file:
            data = json.load(file)
            self.api_key = data['api_key']
            self.api_secret = data['api_secret']
            self.mongo_uri = data['mongo_uri']

    def to_list(self):
        return {
            'api_key': self.api_key,
            'api_secret': self.api_secret,
            'mongo_uri': self.mongo_uri
        }