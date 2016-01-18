"""
Class: StockAnalyst
==============
An analyst takes a (set of stocks, StockMetric) and runs the simulation,
optionally providing an analysis of historical sales
"""
import numpy as np
import pandas as pd
from metrics.stock_metric import StockMetric

class StockAnalyst(object):
    """
    Class: StockAnalyst
    ===================
    Runs StockMetrics on stocks.
    Optionally performs backtesting and comparison against supplied index
    """
    def __init__(self, index_csv='./data/sp_index.csv'):
        self.sp_index = pd.read_csv(index_csv)
        self.sp_index = pd.read_csv('./data/sp_index.csv')[::-1]
        self.sp_index.Date = pd.to_datetime(self.sp_index.Date)
        self.sp_index.index = self.sp_index.Date


    def apply(self, metric, data):
        """runs 'metric' on stock data, returning orders"""
        orders = metric.transform(data)
        return orders

    def evaluate(self, metric, data):
        """
        Evaluates how well metric performs on data
        For every order that could have been executed/completed by now, displays
            displays how well it would have done.

        :param metric: StockMetric to be applied
        :param data: StockChart to apply it to
        :return: modified 'orders' DataFrame with order results inline.
        """
        profits = []
        sell_dates = []
        sell_amts = []
        index_profits = []

        #=====[ Step 1: get orders, iterate over them ]=====
        orders = self.apply(metric, data)
        for ix, order in orders.iterrows():

            #=====[ Step 2: compute some stats ]=====
            buy_amt = order.buy_amt
            buy_date = order.Date

            greater_dates = np.where(order.Date > order.limit_date)[0]
            end_period = date.Date.iloc[greater_dates[0]] if len(greater_dates) > 0 else None # definitely sell by this date
            period = data[order.Date:end_period] if end_period is not None else data[order.Date:]

            below_stops = period.Low < order.stop_below # Pandas returns false here for NaNs
            above_stops = period.High > order.stop_above

            first_below_ix = np.where(below_stops)[0][0] if below_stops.sum() > 0 else np.inf
            first_above_ix = np.where(above_stops)[0][0] if above_stops.sum() > 0 else np.inf

            #=====[ Step 3: determine outcome ]=====
            #####[ CASE: run out the clock ]#####
            if (below_stops.sum() + above_stops.sum()) == 0:
                if order.limit_date > period.Date.max():
                    sell_amt, sell_date = np.nan, np.nan
                else:
                    sell_date_ix = np.where(period.Date >= order.limit_date)[0][0]
                    sell_date = period.iloc[sell_date_ix].Date
                    sell_amt = period.loc[sell_date].Close

            #####[ CASE: stop below ]#####
            elif first_below_ix <= first_above_ix:
                sell_amt = order.stop_below
                sell_date = period.iloc[first_below_ix].Date

            #####[ CASE: stop above ]#####
            else:
                sell_amt = order.stop_above
                sell_date = period.iloc[first_above_ix].Date

            #=====[ Step 4: Calculate profit and return ]=====
            profit = (sell_amt / buy_amt) - 1.0
            profits.append(profit)
            sell_dates.append(sell_date)
            sell_amts.append(sell_amt)

            #=====[ Step 5: calculate index profit in same timeframe ]=====
            if type(sell_date) is pd.tslib.Timestamp:
                index_period = self.sp_index[buy_date:sell_date]
                index_profit = (index_period.iloc[-1].Close - index_period.iloc[0].Open) / index_period.iloc[0].Open
            else:
                index_profit = np.nan
            index_profits.append(index_profit)

        orders['profit'] = profits
        orders['sell_date'] = sell_dates
        orders['sell_amt'] = sell_amts
        orders['index_profit'] = index_profits
        return orders
