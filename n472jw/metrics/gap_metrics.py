"""
Metrics: gaps
=============
"Gaps get filled"
"""
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from stock_metric import StockMetric

class DownGapMetric(StockMetric):
    """
    Metric: DownGapMetric
    =====================
    - gaps going down get filled: implies you should buy
    
    Args:
    -----
    - min_gap_size: minimum size of a gap for it to be considered
    - sell_by: length of max period to hold stock before selling

    #TODO#:
    - min_gap_size should be a percentage of total size
    """
    size = 2 #window size

    def __init__(self, min_gap_size=1, 
                        wait_period=pd.Timedelta('30 days'),
                        stop_below=0.05 #lose a max of 5% before selling
                ):
        self.__dict__.update(locals())

    def ingest(self, window):
        """window has "High" and "Low" columns"""
        downgap_amt = (window.iloc[-1].High - window.iloc[-2].Low)
        buy = downgap_amt < -self.min_gap_size
        stop_above = window.iloc[-2].Low if buy else np.nan
        stop_below = self.stop_below * buy
        return {
            'buy':buy,
            'stop_above':stop_above, 
            'stop_below':stop_below,         # TODO: fill this
            'sell_by':window.index[-1] + self.wait_period
            }
