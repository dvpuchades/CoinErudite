from binance.client import Client
import time
import pymongo
from model import minute
from util import configuration

configuration = configuration.configuration()


#funciones auxiliares
def amount_last_15_minutes(pd_hour, product_name):
    if len(pd_hour) == 0:
        return 0
    amount = 0
    for n in range((len(pd_hour) - 15), len(pd_hour)):
        #empezamos por la 59, la ultima
        amount += pd_hour.iloc[n][product_name]
    return amount

def amount(list):
    amount = 0
    for x in list:
        amount += x
    return amount
#fin



class filler:
    def __init__(self):
        self.client = Client(configuration.binance_api_key, configuration.binance_api_secret)
        self.product_list = ['ethereum', 'cardano', 'dogecoin', 'polkadot', 'ripple', 'bitcoin', 'binance coin', 'uniswap', 'iota', 'luna']
        self.symbol_list = ['ETHBUSD', 'ADABUSD', 'DOGEBUSD', 'DOTBUSD', 'XRPBUSD', 'BTCBUSD', 'BNBBUSD', 'UNIBUSD', 'IOTABUSD', 'LUNABUSD']

    def minute_generator(self):
        mongo_client = pymongo.MongoClient(host=[configuration.mongo_uri])
        db = mongo_client['NN3']
        collection = db['Minutes (Ted)']
        price_list = [[],[],[],[],[]]
        for period in range(15):
            period_time = time.time()
            for s in range(len(self.symbol_list)):
                price_list[s].append(float(self.client.get_symbol_ticker(symbol = self.symbol_list[s])['price']))
            if((time.time() - period_time) < 60):
                time.sleep(60 - (time.time() - period_time))
        while(True):
            init_time = time.time()
            for s in range(len(self.symbol_list)):
                price_list[s].append(float(self.client.get_symbol_ticker(symbol = self.symbol_list[s])['price']))
            dataframe = self.pytrends.interest_over_time()
            for i in range(len(self.product_list)):
                average  = float(self.client.get_avg_price(symbol=self.symbol_list[i])['price'])
                result = price_list[i][15]
                minute_list = price_list[i][10:15]
                average_5 = amount(minute_list) / 5
                average_10 = amount(price_list[i][5:15]) / 10
                average_15 = amount(price_list[i][:15]) / 15
                operation_list = []
                klines = self.client.get_historical_klines(self.symbol_list[i], Client.KLINE_INTERVAL_1MINUTE, "8 minutes ago UTC")
                for x in range(len(klines) - 6, len(klines) - 1):
                    operation_list.append(float(klines[x][8]))
                klines = self.client.get_historical_klines(self.symbol_list[i], Client.KLINE_INTERVAL_1HOUR, "3 hours ago UTC")
                operation_list.append(float(klines[len(klines)-1][8]))
                m = minute.minute(self.product_list[i], self.symbol_list[i], -1, minute_list, average_5, average_10, average_15, average, operation_list)
                m.set_result(result)
                collection.insert_one(m.to_dict()) #insertar en db
                price_list[i].pop()
                print('bip!')
            if((time.time() - init_time) < 60):
                print(str(60 - (time.time() - init_time)) + ' seconds margin')
                time.sleep(60 - (time.time() - init_time))
                