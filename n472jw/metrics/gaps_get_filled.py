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
    """
    def __init__(self, up_threshold=1, down_threshold=1):
        self.__dict__.update(locals())
        
    def transform(self, data):
        #=====[ Step 1: reindex ]=====
        df = data[['Low', 'High', 'Open', 'Close']].copy()
        df['Date'] = df.index
        df.index = range(len(df))

        #=====[ Step 2: find gaps ]=====
        lows = np.array(df.iloc[0:-1].Low)

        down_gap_amounts = (np.array(df[0:-1].Low) - np.array(df[1:].High))
        down_gaps = down_gap_amounts > 0
        up_gap_amounts = (np.array(df[1:].Low) - np.array(df[0:-1].High))
        up_gaps = up_gap_amounts > 0
        up_gaps = (df[1:].Low > df[0:-1].High)

        #=====[ Step 3: reintegrate into series ]=====
        df['down_gap_amount'] = np.nan
        df['down_gap_amount'].iloc[1:] = down_gap_amounts
        df['down_gap'] = df.down_gap_amount > self.down_threshold

        df['up_gap_amount'] = np.nan
        df['up_gap_amount'].iloc[1:] = up_gap_amounts
        df['up_gap'] = df.up_gap_amount > self.up_threshold

        #=====[ Step 4: find occurrences ]=====
        df.index = df['Date']
        df = df.drop(['Date'], axis=1)
        down_df = df[df.down_gap]['down_gap_amount']
        up_df = df[df.up_gap]['up_gap_amount']
        return down_df, up_df
    
    def plot(self, data):
        """finds metrics, plots inline"""
        #=====[ Step 1: find metrics ]=====
        down_df, up_df = self.transform(data)

        #=====[ Step 2: plot metrics ]=====
        data['Open'].plot(color='b', label='open price')
        ax = plt.gca()
        for ix, row in down_df.iteritems():
            ax.axvline(x=ix, color='r', linestyle='--', label='down gap')
        for ix, row in up_df.iteritems():
            ax.axvline(x=ix, color='g', linestyle='--', label='up gap')

        #=====[ Step 3: legend and title ]=====
        ax.legend(loc='lower right')
        ax.set_title('Up and Down Gaps', fontsize=20)