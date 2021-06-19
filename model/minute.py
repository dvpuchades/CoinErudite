import datetime

class minute:
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
        self.result = None
        self.valoration = None
    
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
            'valoration': float(self.valoration)
        }