import redis
from BhavCopy import redis_connection

def get_top_10_stocks_by_code_and_date(r: redis.connection): 
    """
    This function returns the top ten stocks ( according to code ) from redis.
    return: top_10_stocks: list of top ten stocks with their Open, High, Low, Close
    """
    keys = r.keys()
    data = []
    date_of_bhavcopy = None
    for key in keys:
        if key != "date":
            data.append(r.hgetall(key))
        else:   date_of_bhavcopy = r.get(key)
        
    top_10_stocks = sorted(data, key=lambda item: item["OPEN"])[0:10]
    print(top_10_stocks[0:3])
    return top_10_stocks, date_of_bhavcopy


def search_by_name(r : redis,name) -> list:
    """
    This function returns a list of stocks that match with the given string. (Substring search)
    return: The list of stocks which have the given string as a substin in them.
    """
    keys = r.keys("*" + name + "*")
    matching_stocks = []
    for key in keys:
        if key != "date":
            matching_stocks.append(r.hgetall(key))

    return matching_stocks


if __name__ == "__main__":
    r = redis_connection()
    stocks, date = get_top_10_stocks_by_code_and_date(r)
    search_data = search_by_name(r, "REL")
