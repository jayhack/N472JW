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
        
    def ingest(self, data):
    	"""computes internal metrics"""
        raise NotImplementedError("override this")

    def buy_orders(self):
    	"""returns dates to buy on"""
    	raise NotImplementedError

   	def sell_orders(self):
   		"""returns dates to sell on"""
   		raise NotImplementedError

    def stop_orders(self):
    	"""returns stop orders to set"""
    	raise NotImplementedError

    def transform(self):
    	"""returns feature representation of data at intervals"""
    	raise NotImplementedError

    def plot(self):
    	"""returns a graphical representation of what was inferred"""
        raise NotImplementedError("override this")