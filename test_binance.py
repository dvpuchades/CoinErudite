from binance.client import Client
from util import configuration

configuration = configuration.Configuration()

client = Client(configuration.api_key, configuration.api_secret)


info = client.get_account() # Getting account info


print(info)