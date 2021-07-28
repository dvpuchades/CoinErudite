class Day:
    def __init__(self, date, product, price_list, market_cap, operation_list):
        self.date = date
        self.product = product
        self.twitter_followers = 0
        self.reddit_average_posts_48h = 0
        self.reddit_average_comments_48h = 0
        self.alexa_rank = 0
        self.price_list = price_list  #list of the price from the last 5 prices
        self.market_cap = market_cap
        self.operation_list = operation_list #list of the number of operations on the last 5 prices (5) and 1 hour (just one)
        self.result = -1        # -1 as None
        self.valoration = -1    # -1 as None
    
    def set_result(self, result):
        self.result = result
        self.valoration = 0
        if (result > self.price_list[4]):
            self.valoration = 1

    def to_dict(self):
        return {
            'date': self.date,
            'product': str(self.product),
            'twitter_followers': int(self.twitter_followers),
            'reddit_average_posts_48h': float(self.reddit_average_posts_48h),
            'reddit_average_comments_48h': float(self.reddit_average_comments_48h),
            'alexa_rank': int(self.alexa_rank),
            'price_list': self.price_list,
            'market_cap': float(self.market_cap),
            'operation_list': self.operation_list,
            'result': float(self.result),
            'valoration': float(self.valoration)
        }

    
    def to_list(self):
        return flatter([
            self.twitter_followers,
            self.reddit_average_posts_48h,
            self.reddit_average_comments_48h,
            self.alexa_rank,
            self.price_list,
            self.market_cap,
            self.operation_list
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
     m = Day(dict['date'], dict['product'], dict['price_list'], dict['market_cap'], dict['operation_list'])
     m.twitter_followers = dict['twitter_followers']
     m.reddit_average_posts_48h = dict['reddit_average_posts_48h']
     m.reddit_average_comments_48h = dict['reddit_average_comments_48h']
     m.alexa_rank = dict['alexa_rank']
     m.set_result(dict['result'])
     return m