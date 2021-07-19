from binance.client import Client
from util import configuration
import time

configuration = configuration.Configuration()

client = Client(configuration.api_key, configuration.api_secret)
#client.API_URL = 'https://testnet.binance.vision/api' # SOLO PARA TESTING




def get_price_format(symbol_product, priceOrg, quantityOrg):

        # https://stackoverflow.com/questions/61582902/python-binance-api-apierrorcode-1013-filter-failure-lot-size

        price = float(priceOrg)
        quantity = float(quantityOrg)
        response = client.get_symbol_info(symbol_product)
        print(response)
        priceFilterFloat = format(float(response["filters"][0]["tickSize"]), '.20f')
        lotSizeFloat = format(float(response["filters"][2]["stepSize"]), '.20f')
        marketSizeFloat = format(float(response["filters"][5]["stepSize"]), '.20f')
        minNotionalFloat = float(response["filters"][3]["minNotional"])
        print(minNotionalFloat)
        maxMarketSize = float(response["filters"][5]["maxQty"])
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

        # MarketLotSize
        numberAfterDotLot = str(marketSizeFloat.split(".")[1])
        indexOfOneLot = numberAfterDotLot.find("1")
        if indexOfOneLot == -1:
            quantity = int(quantity)
        else:
            quantity = round(float(quantity), int(indexOfOneLot))

        # Quantity
        if quantity < minNotionalFloat:
            return 'invalid quantity'
        if quantity > maxMarketSize:
            return maxMarketSize

        return quantity



info = client.get_account() # Getting account info
print(info)

symbol = 'IOTABUSD'

qty = get_price_format(symbol, 1, 119)

print(qty)

order = client.order_market_sell(
            symbol=symbol,
            quantity= qty)

print(order)