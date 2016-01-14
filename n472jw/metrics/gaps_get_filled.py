"""
StockMetric: GapsGetFilled
==========================
#TODO#
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stock_metric import StockMetric

class GapsGetFilled(StockMetric):
    """
    Metric: GapsGetFilled
    =====================
    - previous day high lower than next day low -> SELL (overbought) 
    - previous day low higher than next day high -> BUY (oversold)
    
    Args:
    -----
    - up_threshold: minimum size of gap on upside
    - down_treshold: minimum size of gap on downside

    #TODO#:
    - thresholds should be a percentage of share price
    """
    def __init__(self, up_threshold=1, down_threshold=1):
        self.__dict__.update(locals())
        
    def ingest(self, data):
        """
        finds buy/sell at current point in time and sell point
        computes self.data, which contains info on up and down
        gaps
        """
        df = data[['Low', 'High', 'Open', 'Close']].copy()
        df['Date'] = df.index
        df.index = range(len(df))

        #=====[ Step 2: find gaps ]=====
        down_gap_amounts = (np.array(df[0:-1].Low) - np.array(df[1:].High))
        down_gap_sell_price = np.array(df[0:-1].Low)
        down_gaps = down_gap_amounts > 0
        up_gap_amounts = (np.array(df[1:].Low) - np.array(df[0:-1].High))
        up_gap_buy_price = np.array(df[0:-1].High)
        up_gaps = up_gap_amounts > 0

        #=====[ Step 3: reintegrate into series ]=====
        df['down_gap_amount'] = np.nan
        df['down_gap_amount'].iloc[1:] = down_gap_amounts
        df['down_gap'] = df.down_gap_amount > self.down_threshold
        df['down_gap_sell_price'] = np.nan
        df['down_gap_sell_price'][1:] = down_gap_sell_price

        df['up_gap_amount'] = np.nan
        df['up_gap_amount'].iloc[1:] = up_gap_amounts
        df['up_gap'] = df.up_gap_amount > self.up_threshold
        df['up_gap_buy_price'] = np.nan
        df['up_gap_buy_price'][1:] = up_gap_buy_price

        #=====[ Step 4: find occurrences ]=====
        df.index = df['Date']
        df = df.drop(['Date'], axis=1)
        self.data = df
    
    def buy_orders(self):
        """returns list of dates to buy on"""
        return df[df.down_gap]

    def plot(self, data=None):
        """finds metrics, plots inline"""
        #=====[ Step 1: ingest if necessary ]=====
        if data is not None:
            self.ingest(data)

        #=====[ Step 2: plot metrics ]=====
        ax = plt.gca()
        self.data.Open.plot(color='b', label='open price')
        for date in self.data[self.data.down_gap].index:
            ax.axvline(x=date, color='r', linestyle='-', label='down gap')
        for date in self.data[self.data.up_gap].index:
            ax.axvline(x=date, color='g', linestyle='-', label='up gap')

        #=====[ Step 3: legend and title ]=====
        ax.legend(loc='lower right')
        ax.set_title('Up and Down Gaps', fontsize=20)