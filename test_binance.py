from binance.client import Client
from util import configuration
import time

configuration = configuration.Configuration()

client = Client(configuration.api_key, configuration.api_secret)
#client.API_URL = 'https://testnet.binance.vision/api' # SOLO PARA TESTING


trades = client.get_historical_trades(symbol='ETHBUSD')
for e in trades:
    print(e)

print(len(trades))