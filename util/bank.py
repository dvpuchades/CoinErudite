from binance.client import Client
from util import configuration
from nn import ted
from model import operation
import datetime
import pymongo
import time
from model import minute
 
configuration = configuration.Configuration()

class Bank:
    def __init__(self, OPERATION_RATIO, STAKE_RATIO, nn):
        self.client = Client(configuration.api_key, configuration.api_secret)
        self.client.API_URL = 'https://testnet.binance.vision/api' # SOLO PARA TESTING
        self.OPERATION_RATIO = OPERATION_RATIO
        self.STAKE_RATIO = STAKE_RATIO
        self.bankroll = 0
        self.info = None
        self.exchange_info = None
        self.set_bankroll()
        self.stake = self.STAKE_RATIO * self.bankroll
        self.pick = self.stake * self.OPERATION_RATIO
        self.nn = nn

        # self.product_list = ['ethereum', 'ripple', 'bitcoin', 'binance coin']
        # self.symbol_list = ['ETHBUSD', 'XRPBUSD', 'BTCBUSD', 'BNBBUSD']
        self.product_list = ['bitcoin', 'binance coin']
        self.symbol_list = ['BTCBUSD', 'BNBBUSD']
        self.operation_list = []

    def set_bankroll(self):
        self.info = self.client.get_account() # Getting account info
        self.bankroll = float(is_BUSD(self.info['balances'])['free'])

    def open_operation(self, product, symbol_product, price):
        # CODIGO ANTIGUO
        # min_qty = get_min_quantity(self.exchange_info, symbol_product, price)
        # if min_qty > self.pick:
        #     quantity = min_qty
        # else:
        #     quantity = self.pick
        quantity = self.get_price_format(symbol_product, price, self.pick / price)
        order = self.client.order_market_buy(
            symbol=symbol_product,
            quantity= quantity)
        op = operation.Operation(product, symbol_product, quantity, order['fills'][0]['price'], order['fills'][0]['commission'])
        self.stake -= quantity
        return op

    def close_operation(self, op, quantity):
        order = self.client.order_market_sell(
            symbol=op.symbol,
            quantity= quantity)
        op.set_sell_price(order['fills'][0]['price'], order['fills'][0]['commission'])
        self.stake += quantity
        return op
    
    def on_air(self):
        mongo_client = pymongo.MongoClient(host=[configuration.mongo_uri])
        db = mongo_client['NN3']
        collection = db['Operations']
        price_list = []
        for s in range(len(self.symbol_list)):
            price_list.append([])
        for period in range(14):
            period_time = time.time()
            for s in range(len(self.symbol_list)):
                price_list[s].append(float(self.client.get_symbol_ticker(symbol = self.symbol_list[s])['price']))
            if((time.time() - period_time) < 60):
                time.sleep(60 - (time.time() - period_time))
        while(True):
            init_time = time.time()
            self.set_bankroll()
            self.exchange_info = self.client.get_exchange_info()

            print('Bankroll: ' + str(self.bankroll))
            for s in range(len(self.symbol_list)):
                price_list[s].append(float(self.client.get_symbol_ticker(symbol = self.symbol_list[s])['price']))
            for i in range(len(self.product_list)):
                average  = float(self.client.get_avg_price(symbol=self.symbol_list[i])['price'])
                minute_list = price_list[i][10:]
                average_5 = amount(minute_list) / 5
                average_10 = amount(price_list[i][5:]) / 10
                average_15 = amount(price_list[i]) / 15
                kline_list = []
                klines = self.client.get_historical_klines(self.symbol_list[i], Client.KLINE_INTERVAL_1MINUTE, "8 minutes ago UTC")
                for x in range(len(klines) - 5, len(klines)):
                    kline_list.append(float(klines[x][8]))
                klines = self.client.get_historical_klines(self.symbol_list[i], Client.KLINE_INTERVAL_1HOUR, "3 hours ago UTC")
                kline_list.append(float(klines[len(klines)-1][8]))
                m = minute.Minute(self.product_list[i], self.symbol_list[i], -1, minute_list, average_5, average_10, average_15, average, kline_list)
                asset = float(is_symbol(self.info['balances'], just_symbol(self.symbol_list[i]))['free'])

                ## Last Valoration ##
                if (price_list[i][-1] - price_list[i][-2]) > 0:
                    print('Last result UP')
                else:
                    print('Last result DOWN')
                ## end ##

                prediction = float(self.nn(m)[0])
                print('Prediction: '+ str(prediction))
                if((prediction > 0.8) and ((self.stake - self.pick) >= 0)):
                    if asset == 0 :
                        ref = generate_ref(i)
                        op = self.open_operation(self.product_list[i], self.symbol_list[i], price_list[i][-1])
                        op.insert_ref(ref)
                        m.ref = ref
                        op.time += 1
                        self.operation_list.append(op)
                    else:
                        ref = generate_ref(i)
                        for op in self.operation_list:
                            if op.symbol == self.symbol_list[i]:
                                op.insert_ref(ref)
                                m.ref = ref
                                op.time += 1
                                break
                        
                else:
                    if asset > 0 :
                        for op in self.operation_list:
                            if op.symbol == self.symbol_list[i]:
                                of = self.close_operation(op, asset)
                                collection.insert_one(of.to_dict()) #insertar en db
                                break
                
                price_list[i].pop()
                print('bip!')
            if((time.time() - init_time) < 60):
                print(str(60 - (time.time() - init_time)) + ' seconds margin')
                time.sleep(60 - (time.time() - init_time))



    def get_price_format(self, symbol_product, priceOrg, quantityOrg):

        # https://stackoverflow.com/questions/61582902/python-binance-api-apierrorcode-1013-filter-failure-lot-size

        price = float(priceOrg)
        quantity = float(quantityOrg)
        response = self.client.get_symbol_info(symbol_product)
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
        

def is_BUSD(l):
    ret = False
    i = -1
    while ret == False:
        i = i + 1
        if l[i]['asset'] == 'BUSD':
            ret = True
    return l[i]

def is_symbol(l, symbol):
    ret = False
    i = -1
    while ret == False:
        i = i + 1
        if l[i]['asset'] == symbol:
            ret = True
    return l[i]

def just_symbol(symbol):
    ret = symbol.split('BUSD')
    return ret[0]

def generate_ref(index):
    d = datetime.datetime.now()
    res = str(d.year) + str(d.month) + str(d.day) + str(d.hour) + str(d.minute) + str(d.second) + str(index)
    return res

def get_min_quantity(info, symbol_product, price):
    for d in info['symbols']:
        if(d['symbol'] == symbol_product):
            for filter in d['filters']:
                if filter['filterType'] == 'LOT_SIZE':
                    qty = float(filter['minQty']) / float(price)
                    qty = qty + (qty * 0.2)
                    return round(qty, 2) # PROBAR Y JUGAR CON LOS DECIMALES
                    break
            break

