from binance.client import Client
from util import configuration
import time
import math

configuration = configuration.Configuration()

client = Client(configuration.api_key, configuration.api_secret)
client.API_URL = 'https://testnet.binance.vision/api' # SOLO PARA TESTING

account_info = client.get_account()
print(account_info)

def get_symbol_index(symbol, info):
    s = symbol.split('USDT')[0]
    i = 0
    for element in info['balances']:
        if element['asset'] == s:
            return i
        i += 1

info = client.get_account() # Getting account info

symbol = 'ETHUSDT'
index = get_symbol_index(symbol, info)

q = float(info['balances'][index]['free'])
while(q > 0):
    order = client.order_market_sell(
                symbol=symbol,
                quantity= q)
    info = client.get_account() # Getting account info
    q = float(info['balances'][index]['free'])
    time.sleep(0.05)
    print(info['balances'][index]['free'])

print(info)