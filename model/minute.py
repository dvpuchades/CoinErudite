import datetime

class Minute:
    def __init__(self, product, symbol, trends, minute_list, average_5, average_10, average_15, average, operation_list):
        self.date = datetime.datetime.now()
        self.product = product
        self.symbol = symbol
        self.trends = trends    #number of search for this product
        self.minute_list = minute_list  #list of the price from the last 5 minutes
        self.average_5 = average_5  
        self.average_10 = average_10
        self.average_15 = average_15
        self.average = average
        self.operation_list = operation_list #list of the number of operations on the last 5 minutes (5) and 1 hour (just one)
        if (operation_list[4] == 0):
            self.operation_rate = 0
        elif (operation_list[5] == 0):
            self.operation_rate = 1
        else:
            self.operation_rate = operation_list[4] / operation_list[5] #(operations) last minute / last hour
        self.result = -1        # -1 as None
        self.valoration = -1    # -1 as None
        self.ref = ''
    
    def set_result(self, result):
        self.result = result
        self.valoration = 0
        if (result > self.minute_list[4]):
            self.valoration = 1

    def to_dict(self):
        return {
            'date': self.date,
            'product': str(self.product),
            'symbol': str(self.symbol),
            'trends': int(self.trends),
            'minute_list': self.minute_list,
            'average_5': float(self.average_5),
            'average_10': float(self.average_10),
            'average_15': float(self.average_15),
            'average': float(self.average),
            'operation_list': self.operation_list,
            'operation_rate': float(self.operation_rate),
            'result': float(self.result),
            'valoration': float(self.valoration),
            'ref': str(self.ref)
        }

    
    def to_list(self):
        return flatter([
            self.trends,
            self.minute_list,
            self.average_5,
            self.average_10,
            self.average_15,
            self.average,
            self.operation_list,
            self.operation_rate
        ])

def flatter(lst):
    ret = []
    for elem in lst:
        if isinstance(elem, list):
            ret.extend(flatter(elem))
        else:
            ret.append(elem)
    return ret

def from_dict(dict):
    m = Minute(dict['product'], dict['symbol'], dict['trends'], dict['minute_list'], dict['average_5'], dict['average_10'], dict['average_15'], dict['average'], dict['operation_list'])
    m.set_result(dict['result'])
    return m