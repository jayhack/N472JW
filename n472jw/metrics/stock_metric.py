"""
Class: StockMetric
==================
Base class for all stock metrics
"""

class StockMetric(object):
    """
    Class: StockMetric
    ==================
    Abstract class that provides a stock metric
    Ingests a list of stock charts and returns a dataframe of "orders"

    #TODO# Formalize what an order is

    Arguments:
    ----------
    - tickers: list of ticker names to operate on

    Input:
    ------
    - a dataframe 
    Returns buy_df, sell_df
    each one has a feature value and (optionally) a sell-price
    
    Usage:
    ------
    buy_df, sell_df = stock_metric.transform(data)
    (each is a list of feature values indexed by dates)
    """
    def __init__(self, *args, **kwargs):
        pass

    def transform(self, data):
        """returns feature representation of window"""
        raise NotImplementedError

    def plot(self, data=None):
        """returns a graphical representation of what was inferred"""
        raise NotImplementedError("override this")