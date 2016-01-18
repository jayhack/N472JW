"""
Class: Scraper
==============
Responsible for retrieving data on all stocks and S&P
"""
import Quandl
import time

class Scraper(object):
    """
    Class: Scraper
    ==============
    Responsible for retrieving data on all stocks and indices
    """
    def __init__(self):
        pass

    def get_stock(self, ticker, wait=True, wait_seconds=1):
        """retrieves data on a specific stock"""
        data = Quandl.get('WIKI/{}'.format(ticker), authtoken=quandl_api_key)
        if wait:
            time.sleep(1)
        return data

    def get_index(self, ticker):
        """returns S&P index for the given date"""