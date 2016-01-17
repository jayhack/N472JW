"""
Metrics: gaps
=============
"Gaps get filled"
"""
import numpy as np
import pandas as pd
from stock_metric import StockMetric

class DownGapMetric(StockMetric):
    """
    Metric: DownGapMetric
    =====================
    - gaps going down get filled: implies you should buy
    
    Args:
    -----
    - self.min_gap_size: minimum size of a gap for it to be considered
    - sell_by: length of max period to hold stock before selling

    #TODO#:
    - self.min_gap_size should be a percentage of total size
    """
    def __init__(self, min_gap_size=0.01, #expressed as a percentage of avg day price
                        max_hold=pd.Timedelta('30 days'),
                        stop_below=0.05 #lose a max of 5% before selling
                ):
        super(self.__class__, self).__init__()
        self.__dict__.update(locals())

    def preprocess(self, data):
        """finds gaps and adds appropriate fields"""
        #=====[ Step 1: get down gap locations ]=====
        data['down_delta'] = np.nan
        data['down_delta'].iloc[1:] = np.array(data.High[1:]) - np.array(data.Low[:-1])
        data['down_gap'] = data['down_delta'] < -(self.min_gap_size * (np.array(data.High - data.Low)/2.0 + np.array(data.Low)))

        #=====[ Step 2: get max price in following days ]=====
        data['stop_above'] = data['High'] - data['down_delta'] #only matters when we cross
        data['stop_below'] = data['Close'] * (1.0 - self.stop_below)
        data['limit_date'] = data.index + self.max_hold
        return data

    def transform(self, data):
        #=====[ Step 1: find all gaps ]=====
        data = self.preprocess(data.copy())

        #=====[ Step 2: make and return orders ]=====
        orders = data[data.down_gap][['Date', 'Close', 'limit_date', 'stop_above', 'stop_below']]
        orders = orders.rename(columns={'Close':'buy_amt'})
        return orders



