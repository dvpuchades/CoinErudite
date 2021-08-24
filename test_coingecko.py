from pycoingecko import CoinGeckoAPI
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
                    return '28-2-' + str(year)
                else:
                    return '30-'+ str(month - 1) +'-' + str(year)
    else:
        return str(day - 1)+'-'+str(month)+'-'+str(year)

day = '27-07-2021'

for i in range(1):
    data = cg.get_coin_history_by_id(id='ethereum', date=day)
    print(day)
    print(data)
    #print(data['market_data']['current_price']['usd'])
    day = get_one_day_ago(day)