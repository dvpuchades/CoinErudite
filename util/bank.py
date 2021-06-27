from binance.client import Client
from util import configuration
from nn import ted
from model import operation
import asyncio
import datetime

configuration = configuration.Configuration()

class Bank:
    def __init__(self, OPERATION_RATIO, STAKE_RATIO):
        self.client = Client(configuration.api_key, configuration.api_secret)
        self.OPERATION_RATIO = OPERATION_RATIO
        self.STAKE_RATIO = STAKE_RATIO
        self.bankroll = 0
        self.info = None
        self.set_bankroll()
        self.stake = self.STAKE_RATIO * self.bankroll
        self.pick = self.stake * self.OPERATION_RATIO
        self.nn = ted.Ted()

        self.product_list = ['ethereum', 'cardano', 'dogecoin', 'polkadot', 'ripple', 'bitcoin', 'binance coin', 'uniswap', 'iota', 'luna coin']
        self.symbol_list = ['ETHBUSD', 'ADABUSD', 'DOGEBUSD', 'DOTBUSD', 'XRPBUSD', 'BTCBUSD', 'BNBBUSD', 'UNIBUSD', 'IOTABUSD', 'LUNABUSD']
        self.operation_list = []

    def set_bankroll(self):
        self.info = self.client.get_account() # Getting account info
        self.bankroll = float(is_BUSD(info['balances'])['free'])

    async def open_operation(self, product, symbol_product):
        quantity = self.pick
        order = client.order_market_buy(
            symbol=symbol_product,
            quantity= quantity)
        op = operation.Operation(product, symbol_product, quantity, order['fills'][0]['price'], order['fills'][0]['commission'])
        self.stake -= quantity
        return op

    async def close_operation(self, op, quantity):
        order = client.order_market_sell(
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
                if(self.nn(m) > 0.5 & (self.stake - self.pick) >= 0):
                    asset = float(is_symbol(info['balances'], just_symbol(self.symbol_list[i]))['free'])
                    if asset == 0 :
                        ref = generate_ref(i)
                        op = self.open_operation(self.product_list[i], self.symbol_list[i])
                        op.insert_ref(ref)
                        m.ref = ref
                        self.operation_list.append(op)
                    else:
                        ref = generate_ref(i)
                        for op in self.operation_list:
                            if op.symbol == self.symbol_list[i]:
                                op.insert_ref(ref)
                                m.ref = ref
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