from pycoingecko import CoinGeckoAPI
from util import configuration
import pymongo
import time
from model.day import Day

configuration = configuration.Configuration()
mongo_client = pymongo.MongoClient(host=[configuration.mongo_uri])
db = mongo_client['NN3']
collection = db['Days']


cg = CoinGeckoAPI()

def get_one_day_ago(str_day):
    list_day = str_day.split('-')

    day = int(list_day[0])
    month = int(list_day[1])
    year = int(list_day[2])

    if day == 1:
        if month == 1:
            return '31-12-' + str(year - 1)
        else:
            if month in [4, 6, 8, 9, 11]:
                return '31-'+ str(month - 1) +'-' + str(year)
            else:
                if month == 3:
                    if year % 4 == 0:
                        return '29-2-' + str(year)
                    return '28-2-' + str(year)
                else:
                    return '30-'+ str(month - 1) +'-' + str(year)
    else:
        return str(day - 1)+'-'+str(month)+'-'+str(year)

day = '28-07-2021'

data_list = []

for i in range(2000):
    data = cg.get_coin_history_by_id(id='bitcoin', date=day)
    data_list.append([day, data])
    day = get_one_day_ago(day)
    if(len(data_list) == 91):
        date = data_list[1][0]
        product = 'bitcoin'

        price_list = []
        for j in range(5, 0, -1):
            price_list.append(float(data_list[j][1]['market_data']['current_price']['usd']))
        
        market_cap =float(data_list[0][1]['market_data']['market_cap']['usd'])

        average_15 = 0
        for j in range(1, 16):
            average_15 += float(data_list[j][1]['market_data']['current_price']['usd']) / 15

        average_30 = 0
        for j in range(1, 31):
            average_30 += float(data_list[j][1]['market_data']['current_price']['usd']) / 30

        average_90 = 0
        for j in range(1, 91):
            average_90 += float(data_list[j][1]['market_data']['current_price']['usd']) / 90
        
        result = float(data_list[0][1]['market_data']['current_price']['usd'])

        d = Day(date, product, price_list, market_cap, average_15, average_30, average_90)

        d.twitter_followers = int(data_list[1][1]['community_data']['twitter_followers'])
        d.reddit_average_posts_48h = float(data_list[1][1]['community_data']['reddit_average_posts_48h'])
        d.reddit_average_comments_48h = float(data_list[1][1]['community_data']['reddit_average_comments_48h'])
        d.alexa_rank = int(data_list[1][1]['public_interest_stats']['alexa_rank'])

        d.set_result(result)
        
        collection.insert_one(d.to_dict()) #insertar en db

        data_list.pop(0)

    time.sleep(3)
