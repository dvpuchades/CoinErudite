import datetime

class operation:
    def __init__(self, product, symbol, buy_price):
        self.date = datetime.datetime.now()
        self.product = product
        self.symbol = symbol
        self.buy_price = buy_price
        self.time = 0   # time in minutes
        self.sell_price = 0
        self.earning = 0
        self.valoration = 0

    def set_sell_price(self, sell_price):
        self.sell_price = sell_price
        self.earning = self.buy_price - self.sell_price
        if(self.earning > 0):
            self.valoration = 1
    
    def to_dict():
        return {
            'date': self.date,
            'product': str(self.product),
            'symbol': str(self.symbol),
            'buy_price': float(self.buy_price),
            'time': int(self.time),
            'sell_price': float(self.sell_price),
            'earning': float(self.earning),
            'valoration': float(self.valoration)
        }