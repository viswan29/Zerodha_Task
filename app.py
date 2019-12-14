import datetime
import cherrypy
import redis
from BhavCopy import Bhavcopy_bse_downloader
from Models import search_by_name, get_top_10_stocks_by_code_and_date

from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader("templates"))


class Top_10_Stocks(object):

    @cherrypy.expose
    def index(self):
        """
        This is the index route that shows top 10 stocks
        """
        r = redis.StrictRedis(host="127.0.0.1",port=6379,decode_responses=True)
        top_10_stocks, date = get_top_10_stocks_by_code_and_date(r=r)
        tmpl = env.get_template("top_10_stocks.html")
        return tmpl.render(top_10_stocks=top_10_stocks, date=date)

    @cherrypy.expose
    def BhavCopy_for_date(self, date_string):
        """
        This route is used to run bhavcopy for a given date.
        return: html template 
        """
        date_obj = datetime.datetime.strptime(date_string, "%Y-%m-%d").date()
        records = Bhavcopy_bse_downloader(date=date_obj)
        r = redis.StrictRedis(host="127.0.0.1",port=6379,decode_responses=True)
        if len(records)>0:
            for record in records:
                r.hmset(record["SC_NAME"], record)
        else:
            r.flushall()
        r.set("date", date_string)
        raise cherrypy.HTTPRedirect("/")

    @cherrypy.expose
    def stock_search(self, stock_search_string):
        """
        This is the search route for matching the given string with the list of stocks present in the database.
        return: html template
        """
        r = redis.StrictRedis(host="127.0.0.1",port=6379,decode_responses=True)
        stocks = search_by_name(r, name=stock_search_string)
        tmpl = env.get_template("stock_search.html")
        date = r.get("date")
        return tmpl.render(stocks=stocks, stock_search_string=stock_search_string, date=date)


if __name__ == "__main__":
    cherrypy.quickstart(Top_10_Stocks())