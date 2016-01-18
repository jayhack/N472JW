"""
StockMetric: CrossingMovingAverages
===================================
#TODO#
"""
import numpy as np
import pandas as pd
from stock_metric import StockMetric

class CrossingMovingAverages(StockMetric):
    """
    Metric: CrossingMovingAverages
    ==============================
    Returns buy orders when moving averages cross

    Args:
    -----
    - ma1: number of days over which to calculate MA1
    - ma2: number of days over which to calculate MA2
    """

    def __init__(self, ma1=50, ma2=200, wait_period=pd.Timedelta('30 days')):
        super(self.__class__, self).__init__()
        self.__dict__.update(locals())

    def preprocess(self, data):
        """updates 'data' to contain mas, crossovers"""
        #=====[ Step 1: find crossovers ]=====
        data['ma1'] = pd.rolling_mean(data.Open, 200)
        data['ma2'] = pd.rolling_mean(data.Open, 50)
        data['under'] = data['ma2'] <= data['ma1']
        data['over'] = data['ma2'] > data['ma1']
        x = data[['under', 'over']].astype(np.float64)
        data['crossover'] = pd.rolling_mean(x.under - x.over, 2)
        data['crossover'].loc[data['ma1'].isnull()] = np.nan
        data['crossover'] = (data.crossover == 0)
        data['crossup'] = data.crossover & (data['ma2'] > data['ma1'])
        return data

    def transform(self, data):
        #=====[ Step 1: preprocess data ]=====
        data = self.preprocess(data.copy())

        #=====[ Step 2: make orders ]====
        orders = []
        for ts, row in data[data.crossup].iterrows():
            order = {
                'Date':row.Date,
                'buy_amt':np.mean([row.Open, row.Close]), # buy when it crosses over 200 day moving average
                'stop_above':np.nan,
                'stop_below':np.nan,
                'limit_date': ts + self.wait_period
            }
            orders.append(order)
        return pd.DataFrame(orders)

    #def plot(self, data):
    #   #=====[ Step 1: get metrics ]=====
    #   ma_1, ma_2 = self.get_mas(data)
    #   up_crosses, down_crosses = self.transform(data)

    #   #=====[ Step 2: plot MAs ]=====
    #   data['Open'].plot(label='open price', color='b')
    #   ma_1.plot(label='{} day MA'.format(self.ma1), color='g', linestyle='-')
    #   ma_2.plot(label='{} day MA'.format(self.ma2), color='r', linestyle='-')
    #   ax = plt.gca()
    #
    #   #=====[ Step 3: plot crosses ]=====
    #   for ix, row in down_crosses.iteritems():
    #       ax.axvline(x=ix, color='r', linestyle='--', label='down cross')
    #   for ix, row in up_crosses.iteritems():
    #       ax.axvline(x=ix, color='g', linestyle='--', label='up cross')

    #   #=====[ Step 4: legend ]=====
    #   ax.legend(loc='lower right')
    #   ax.set_title('{}/{} MAs Crossing'.format(self.ma1, self.ma2), fontsize=20)