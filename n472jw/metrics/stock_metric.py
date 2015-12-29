"""
Class: StockMetric
==================
Base class for all stock metrics
"""

class StockMetric(object):
    """
    Class: StockMetric
    ==================
    Abstract class that provides a stock metric;
    
    Usage:
    ------
    buy_df, sell_df = stock_metric.transform(data)
    (each is a list of feature values indexed by dates)
    """
    def __init__(self, *args, **kwargs):
        pass
        
    def transform(self):
        raise NotImplementedError("override this")

    def plot(self):
        raise NotImplementedError("override this")