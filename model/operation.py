import datetime

class Operation:
    def __init__(self, product, symbol, quantity, buy_price, buy_commission):
        self.date = datetime.datetime.now()
        self.product = product
        self.symbol = symbol
        self.quantity = quantity
        self.buy_price = buy_price
        self.buy_commission = buy_commission
        self.time = 0   # time in minutes
        self.sell_price = 0
        self.earning = 0
        self.valoration = 0
        self.state = 'open'
        self.fills = [] # aux to sell in different operations 
        self.ref = []

    def set_sell_price(self, fills_info):
        qty = 0
        price = 0
        commission = 0
        for d in fills_info:
            price += d['price']*d['qty']
            commission += d['commission']*d['qty']
            qty += d['qty']
        if price > 0:
            price = price / qty
        if commission > 0:
            commission = commission / qty
        self.sell_price = price
        self.sell_commission = commission
        self.earning = (self.sell_price * (self.quantity - self.buy_commission) / self.buy_price) - self.sell_commission - self.quantity
        if(self.earning > 0):
            self.valoration = 1

    def insert_ref(self, ref):
        self.ref.append(ref)
    
    def to_dict():
        return {
            'date': self.date,
            'product': str(self.product),
            'symbol': str(self.symbol),
            'quantity': float(self.quantity),
            'buy_price': float(self.buy_price),
            'buy_commission': float(self.buy_commission),
            'time': int(self.time),
            'sell_price': float(self.sell_price),
            'sell_commission': float(self.sell_commission),
            'earning': float(self.earning),
            'valoration': float(self.valoration),
            'ref': self.ref
        }