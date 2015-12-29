"""
StockMetric: CrossingMovingAverages
===================================
#TODO#
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stock_metric import StockMetric

class CrossingMovingAverages(StockMetric):
    """
    Metric: CrossingMovingAverages
    ==============================
    MA 1 crosses over MA 2 -> buy
    MA 1 crosses under MA 2 -> sell

    Args:
    -----
    - ma1: number of days over which to calculate MA1
    - ma2: number of days over which to calculate MA2
    """
    def __init__(self, ma1=50, ma2=200):
        self.__dict__.update(locals())

    def get_mas(self, data):
        """returns MA1, MA2"""
        df = data[['Low', 'High', 'Open', 'Close']].copy()
        df['Date'] = df.index
        ma_1 = pd.rolling_mean(df.Open, self.ma1)
        ma_2 = pd.rolling_mean(df.Open, self.ma2)
        return ma_1, ma_2

    def transform(self, data):
        #=====[ Step 1: get MAs ]=====
        ma_1, ma_2 = self.get_mas(data)

        #=====[ Step 2: find crossings ]====
        diff = ma_1 - ma_2
        up_crosses = pd.rolling_apply(diff, 2, lambda x: (x[0] < 0) & (x[-1] > 0))
        up_crosses = up_crosses[up_crosses > 0]
        down_crosses = pd.rolling_apply(diff, 2, lambda x: (x[0] > 0) & (x[-1] < 0))
        down_crosses = down_crosses[down_crosses > 0]
        return up_crosses, down_crosses
    
    def plot(self, data):
        #=====[ Step 1: get metrics ]=====
        ma_1, ma_2 = self.get_mas(data)
        up_crosses, down_crosses = self.transform(data)

        #=====[ Step 2: plot MAs ]=====
        data['Open'].plot(label='open price', color='b')
        ma_1.plot(label='{} day MA'.format(self.ma1), color='g', linestyle='-')
        ma_2.plot(label='{} day MA'.format(self.ma2), color='r', linestyle='-')
        ax = plt.gca()
        
        #=====[ Step 3: plot crosses ]=====
        for ix, row in down_crosses.iteritems():
            ax.axvline(x=ix, color='r', linestyle='--', label='down cross')
        for ix, row in up_crosses.iteritems():
            ax.axvline(x=ix, color='g', linestyle='--', label='up cross')

        #=====[ Step 4: legend ]=====
        ax.legend(loc='lower right')
        ax.set_title('{}/{} MAs Crossing'.format(self.ma1, self.ma2), fontsize=20)