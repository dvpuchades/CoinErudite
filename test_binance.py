from binance.client import Client
from util import configuration
import time

configuration = configuration.Configuration()

client = Client(configuration.api_key, configuration.api_secret)
client.API_URL = 'https://testnet.binance.vision/api' # SOLO PARA TESTING




def get_price_format(symbol_product, priceOrg, quantityOrg):

    # https://stackoverflow.com/questions/61582902/python-binance-api-apierrorcode-1013-filter-failure-lot-size

    price = float(priceOrg)
    quantity = float(quantityOrg)
    response = client.get_symbol_info(symbol_product)
    priceFilterFloat = format(float(response["filters"][0]["tickSize"]), '.20f')
    lotSizeFloat = format(float(response["filters"][2]["stepSize"]), '.20f')
    # PriceFilter
    numberAfterDot = str(priceFilterFloat.split(".")[1])
    indexOfOne = numberAfterDot.find("1")
    if indexOfOne == -1:
        price = int(price)
    else:
        price = round(float(price), int(indexOfOne - 1))
    # LotSize
    numberAfterDotLot = str(lotSizeFloat.split(".")[1])
    indexOfOneLot = numberAfterDotLot.find("1")
    if indexOfOneLot == -1:
        quantity = int(quantity)
    else:
        quantity = round(float(quantity), int(indexOfOneLot))
    
    return quantity




stake = 100

pick = 100 * 0.05

price = float(client.get_symbol_ticker(symbol = 'BNBBUSD')['price'])

qty = get_price_format('BNBBUSD', price, pick / price)

order = client.order_market_buy(
            symbol='BNBBUSD',
            quantity= qty)

print(order)