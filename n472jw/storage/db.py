"""
Class: DB
=========
Manages storage of all data
"""
from os import listdir
from os.path import join
from os import remove
from tqdm import tqdm
import random
import pandas as pd

class DB(object):
    """
    Class: DB
    =========
    Manages storage of all data
    """
    def __init__(self, data_dir='./data/'):
        self.data_dir = data_dir
        self.charts = {}

    def available_tickers(self):
        """returns set of all available tickers"""
        return [x.split('.')[0] for x in listdir(self.data_dir) if x.endswith('.pkl')]

    def save_chart(self, ticker, data):
        """saves a chart to disk"""
        data.to_pickle(join(self.data_dir, '{}.pkl'.format(ticker)))

    def load_chart(self, ticker):
        """loads chart from disk"""
        return pd.read_pickle(join(self.data_dir, '{}.pkl'.format(ticker)))

    def load_random_chart(self):
        """loads/returns random ticker, chart"""
        ticker = random.choice(self.available_tickers())
        return ticker, self.load_chart(ticker)

    def load_charts(self, subset=-1):
        #=====[ Step 1: grab all relevant tickers ]=====
        if subset is not -1:
            tickers = self.available_tickers()[:subset]
        else:
            tickers = self.available_tickers()

        #=====[ Step 2: load into memory ]=====
        print 'Loading tickers:'
        for ticker in tqdm(tickers):
            data = self.load_chart(ticker)
            if len(data) > 0:
                self.charts[ticker] = data
            else:
                remove(join(self.data_dir, '{}.pkl'.format(ticker)))
        return self.charts
