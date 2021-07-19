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
        mongo_client = pymongo.MongoClient(host=[configuration.mongo_uri])
        self.db = mongo_client['NN3']
        self.operations_collection = self.db['Operations']

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
        self.product_list = ['cardano', 'polkadot', 'uniswap', 'iota', 'luna coin']
        self.symbol_list = ['ADABUSD', 'DOTBUSD', 'UNIBUSD', 'IOTABUSD', 'LUNABUSD']
        self.operation_list = []
        self.suspended_operations = [] # SEGUIR AQUI

        self.price_list = []
        self.kline_list = []


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
        if str(quantity) == 'invalid quantity':
            return None
        order = self.client.order_market_buy(
            symbol=symbol_product,
            quantity= quantity)
        if(order['fills'] == []):
            return None
        op = operation.Operation(product, symbol_product, quantity, order['fills'][0]['price'], order['fills'][0]['commission'])
        self.stake -= quantity
        print('Opened!' + symbol_product)
        return op

    def close_operation(self, op):
        index = get_symbol_index(op.symbol, self.info)
        print('Closing ' + op.product)
        quantity = self.get_price_format(op.symbol, 1.0, float(self.info['balances'][index]['free']))
        if str(quantity) == 'invalid quantity':
            op.state = 'suspended'
            return op

        order = self.client.order_market_sell(
            symbol= op.symbol,
            quantity= quantity)

        op.state = 'closing'

        if(order['fills'] != []):
            op.fills += order['fills']
            price = order['fills'][-1]['price']
            self.set_bankroll()
            self.stake += quantity * price
            quantity = float(self.info['balances'][index]['free'])
            if quantity == 0:
                op.state = 'closed'
                op.set_sell_price(op.fills)
                print('Closed!' + op.symbol)
            else:
                self.stake -= quantity * price

        return op

    
    def get_minutes(self):
        minutes = []
        if self.price_list == []:
            for s in range(len(self.symbol_list)):
                self.price_list.append([])
            for period in range(15):
                period_time = time.time()
                for s in range(len(self.symbol_list)):
                    self.price_list[s].append(float(self.client.get_symbol_ticker(symbol = self.symbol_list[s])['price']))
                if((time.time() - period_time) < 60):
                    time.sleep(60 - (time.time() - period_time))

        # inconditional code
        for s in range(len(self.symbol_list)):
            self.price_list[s].pop(0)
            self.price_list[s].append(float(self.client.get_symbol_ticker(symbol = self.symbol_list[s])['price']))
        for i in range(len(self.product_list)):
            average  = float(self.client.get_avg_price(symbol=self.symbol_list[i])['price'])
            minute_list = self.price_list[i][10:]
            average_5 = amount(minute_list) / 5
            average_10 = amount(self.price_list[i][5:]) / 10
            average_15 = amount(self.price_list[i]) / 15
            kline_list = []
            klines = self.client.get_historical_klines(self.symbol_list[i], Client.KLINE_INTERVAL_1MINUTE, "8 minutes ago UTC")
            for x in range(len(klines) - 5, len(klines)):
                kline_list.append(float(klines[x][8]))
            klines = self.client.get_historical_klines(self.symbol_list[i], Client.KLINE_INTERVAL_1HOUR, "3 hours ago UTC")
            kline_list.append(float(klines[len(klines)-1][8]))
            m = minute.Minute(self.product_list[i], self.symbol_list[i], -1, minute_list, average_5, average_10, average_15, average, kline_list)
            minutes.append(m)
        return minutes


    def evaluate_minutes(self, minutes):
        evaluation = []
        for m in minutes:
            evaluation.append(float(self.nn(m)[0]))
        return evaluation


    def take_decisions(self, evaluation):
        #   primera iteración
        if self.operation_list == []:
            for i in range(len(self.symbol_list)):
                self.operation_list.append(None)
        #   cualquier iteración
        for i in range(len(self.symbol_list)):
            if(evaluation[i] > 0.8):
                #   código para pronóstico positivo
                if (self.operation_list[i] == None) and ((self.stake - self.pick) >= 0):
                    op = self.open_operation(self.product_list[i], self.symbol_list[i], self.price_list[i][-1])
                    self.operation_list[i] = op

            else:
                #   código para pronóstico negativo
                if self.operation_list[i] != None:
                    op = self.close_operation(self.operation_list[i], self.price_list[i][-1])
                    if (op.state == 'closed'):
                        self.operation_list[i] = None
                        self.operations_collection.insert_one(op.to_dict())
                    if  (op.state == 'suspended'):
                        self.operation_list[i] = None
                        self.operations_collection.insert_one(op.to_dict())
                        self.suspended_operations.append(op)
                    else:
                        self.operation_list[i] = op

    def try_suspended_operations(self):
        so = []
        for op in self.suspended_operations:
            op = self.close_operation(op, get_price_index(op.symbol, self.symbol_list))
            if (op.state == 'closed'):
                self.operations_collection.insert_one(op.to_dict())
            if  (op.state == 'suspended'):
                so.append(op)
        self.suspended_operations = so
    


    def on_air(self):
        while True:
            init_time = time.time()
            minutes = self.get_minutes()
            evaluation = self.evaluate_minutes(minutes)
            self.take_decisions(evaluation)
            self.try_suspended_operations()

            ejecution_time = time.time() - init_time
            if ejecution_time < 60:
                time.sleep(60 - ejecution_time)



    def get_price_format(self, symbol_product, priceOrg, quantityOrg):

        # https://stackoverflow.com/questions/61582902/python-binance-api-apierrorcode-1013-filter-failure-lot-size

        price = float(priceOrg)
        quantity = float(quantityOrg)
        response = self.client.get_symbol_info(symbol_product)
        priceFilterFloat = format(float(response["filters"][0]["tickSize"]), '.20f')
        lotSizeFloat = format(float(response["filters"][2]["stepSize"]), '.20f')
        marketSizeFloat = format(float(response["filters"][5]["stepSize"]), '.20f')
        minNotionalFloat = float(response["filters"][3]["minNotional"])
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
        if quantity < minNotionalFloat / price:
            return 'invalid quantity'
        if quantity > maxMarketSize:
            return maxMarketSize

        return quantity


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


def get_symbol_index(symbol, info):
    s = symbol.split('BUSD')[0]
    i = 0
    for element in info['balances']:
        if element['asset'] == s:
            return i
        i += 1

def get_price_index(symbol, symbol_list):
    i = -1
    for s in symbol_list:
        i += 1
        if s == symbol:
            return i
    return -1