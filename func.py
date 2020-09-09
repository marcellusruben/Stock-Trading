# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from stockstats import StockDataFrame as sdf
from datetime import datetime
import plotly.graph_objs as go
#import plotly.io as pio
#pio.renderers.default = "browser"

# Read file and preprocess the data

def file_reading(filename, rolling_window, time_begin, time_end, indicators, mov_avg):
    
    df = pd.read_csv(filename)
    

    df['Date'] = pd.to_datetime(df['Date'])
    df['VWAP'] = df['VWAP'].rolling(rolling_window).mean()
    
    df = df.set_index(['Datetime'])
    df = df.loc[str(time_begin):str(time_end)]
    
    df.reset_index(inplace=True)
    
    s_df = sdf.retype(df)
    
    if indicators == 'macd':
        s_df.get(indicators)
        
    elif indicators == 'rsi':
        s_df.get(indicators+'_'+str(mov_avg))
    
    elif indicators == 'bb':
        
        BB(s_df)
    
    return s_df

# Formula for Bollinger Band
    
def BB(df):
    
    df['sma'] = df['close'].rolling(window = 20).mean()
    rstd = df['close'].rolling(window = 20).std()
    df['upper_band'] = df['sma'] + 2 * rstd
    df['lower_band'] = df['sma'] - 2 * rstd

# Process the user input parameters    

class UserParameters(object):
    
    def __init__(self):
        
        self.filename_daily = 'x'
        self.filename_hourly = 'x'
        self.time_begin = datetime.strptime(str('2020-01-01') , '%Y-%m-%d')
        self.time_end = datetime.strptime(str('2020-06-01') , '%Y-%m-%d')
        self.option_time = 'daily'
        self.stock_add = 8
        self.indicator = 'macd'
        self.vwap_window_daily = 15
        self.vwap_window_hourly = 105
        self.rsi_mov_avg_hourly = 14
        self.rsi_mov_avg_daily = 7
        self.overbought = 80
        self.oversold = 20
        
    def set_parameters(self, variable, value):
    
        if variable == 'daily_filename':
            self.filename_daily = str(value)
    
        if variable == 'hourly_filename':
            self.filename_hourly = str(value)
        
        if variable == 'start_date':
            self.time_begin = datetime.strptime(str(value) , '%Y-%m-%d')
    
        if variable == 'end_date':
            self.time_end = datetime.strptime(str(value) , '%Y-%m-%d')
    
        if variable == 'timeframe_viz':
            self.option_time = str(value).lower()
    
        if variable == 'trading_style':
            trading_style = (str(value)).lower()
        
            if trading_style == 'risk_taking':
                self.stock_add = 8
        
            elif trading_style == 'risk_averse':
                self.stock_add = 4
    
        if variable == 'indicator':
            option_ind = (str(value)).lower()
        
            if option_ind == 'macd':    
                self.indicator = 'macd'
        
            elif option_ind == 'rsi':    
                self.indicator = 'rsi'
            
            elif option_ind == 'bb':    
                self.indicator = 'bb'
                
            if self.indicator == 'rsi':
                self.rsi_mov_avg_hourly = int(input('Input Hourly MA RSI (default 14).Just press enter if you agree with default value: ') or "14")
                self.rsi_mov_avg_daily = int(input('Input Daily MA RSI (default 7). Just press enter if you agree with default value: ') or "7")
                self.overbought = int(input('Input Overbought Threshold (default 80). Just press enter if you agree with default value: ') or "80")
                self.oversold = int(input('Input Oversold Threshold (default 20). Just press enter if you agree with default value: ') or "20")
                
                    
    
        if variable == 'daily_vwap':
            self.vwap_window_daily = int(value)
    
        if variable == 'hourly_vwap':
            self.vwap_window_hourly = int(value)
        
    def read_file(self, filepath):      


        file = open(filepath + '/InputParam.txt','r')

        inputfile = file.readlines()
       

        for line in inputfile: 
         
            linelist = line.split()
            if len(linelist) == 2:
                self.set_parameters(linelist[0].lower(), linelist[1])

# Process the hourly data at specific date
                
class DataFeed(object):
    
    def __init__(self, df, history, indicators, mov_avg):
        
        self.df = df
        self.indicators = indicators
        self.history = history
        self.mov_avg = mov_avg
        
    def get_values(self):
        
        self.date = self.df['date']
        self.open = self.df['open']
        self.high = self.df['high']
        self.low = self.df['low']
        self.close = self.df['close']
        self.volume = self.df['volume']
        self.vwap = self.df['vwap']
        self.datetime = self.df['datetime']
        
        self.values = [self.date, self.open, self.high, self.low, self.close, self.volume, self.vwap, self.datetime]
        
        return self.values

    def get_indicators(self):
        
        if self.indicators == 'macd':
        
            self.macd = self.df['macd']
            self.macds = self.df['macds']
            
            self.macd_all = [self.macd, self.macds]
            
            return self.macd_all
    
        elif self.indicators == 'rsi':
            
            self.rsi = self.df[self.indicators+'_'+str(self.mov_avg)]
            
            return self.rsi
        
        elif self.indicators == 'bb':
            
            self.sma = self.df['sma']
            self.upper_band = self.df['upper_band']
            self.lower_band = self.df['lower_band']
            self.close = self.df['close']
            
            self.bb = [self.close, self.upper_band, self.lower_band]
            
            return self.bb
        
        
    def get_history(self):
        
        return self.history.append(self.values)
    
# Perform trading algorithm
        
class Trader(object):
    
    def __init__(self, df_hourly, df_daily, indicators, mov_avg_daily, mov_avg_hourly, overbought, oversold, rolling_window, stock_add):
        
        self.df_hourly = df_hourly
        self.df_daily = df_daily
        self.indicators = indicators
        self.rolling_window = rolling_window
        self.mov_avg_daily = mov_avg_daily
        self.mov_avg_hourly = mov_avg_hourly
        self.overbought = overbought
        self.oversold = oversold
        self.stock_add = stock_add
    
    # Check state whether there is a momentum reversal
        
    def state_check(self, value, indicators):
        
        if indicators == 'macd':
            
            state_check = lambda x, y: 1 if x > y else 0
            self.state = state_check(value[0], value[1])
            
        elif indicators == 'rsi':
            
            state_check = lambda x:1 if x > self.overbought or x < self.oversold else 0
            self.state = state_check(value)
        
        elif indicators == 'bb':
            
            state_check = lambda x, y, z: 1 if abs(1 - x/z) < 0.02 or abs(1 - y/x) < 0.02 else 0
            self.state = state_check(value[0], value[1], value[2])
        
        
        return self.state
    
    # Trading conditions
    
    def trading_rules(self, ohlc_value, indicator_value_hourly, indicator_value_daily, indicators, stock_left, max_stock_amt, stock_amt, profit, transaction):
        
        if indicators == 'macd':
            
            self.buy_condition = ((indicator_value_hourly[0] > indicator_value_hourly[1]) and (indicator_value_daily[0] > indicator_value_daily[1]) and stock_left != 0)
            self.sell_condition = ((indicator_value_hourly[0] < indicator_value_hourly[1]) and (indicator_value_daily[0] < indicator_value_daily[1]) and stock_amt != 0)
            
            
        elif indicators == 'rsi':
            
            self.buy_condition = ((indicator_value_hourly < self.oversold) and (indicator_value_daily < self.oversold) and stock_left != 0)
            self.sell_condition = ((indicator_value_hourly > self.overbought) and (indicator_value_daily > self.overbought) and stock_amt != 0)
            
        elif indicators == 'bb':
            
       
            self.buy_condition = ((abs(1 - ohlc_value[4]/indicator_value_hourly[2]) < 0.02) and stock_left != 0)
            self.sell_condition = ((abs(1 - indicator_value_hourly[1]/ohlc_value[4]) < 0.02) and stock_amt != 0)
            
        
        if self.buy_condition == True:
            
            
            if (ohlc_value[4] < ohlc_value[6]):
                
                stock_amt += stock_left
                profit = profit - (stock_left * ohlc_value[4])
                self.transaction.append([ohlc_value[0], ohlc_value[4], 1, profit, stock_amt, ohlc_value[7]])
                
            elif (stock_left >= self.stock_add):
            
                stock_amt += self.stock_add
                profit = profit - (self.stock_add * ohlc_value[4])
                self.transaction.append([ohlc_value[0], ohlc_value[4], 1, profit, stock_amt, ohlc_value[7]])
                            
            else:

                stock_amt += 2
                profit = profit - (2 * ohlc_value[4])
                self.transaction.append([ohlc_value[0], ohlc_value[4], 1, profit, stock_amt, ohlc_value[7]])
        
        if self.sell_condition == True:
            
        
            if (ohlc_value[4] > ohlc_value[6]):
                
                profit = profit + (stock_amt * ohlc_value[4])
                stock_amt -= stock_amt
                self.transaction.append([ohlc_value[0], ohlc_value[4], 0, profit, stock_amt, ohlc_value[7]])
                        
            elif (stock_amt >= self.stock_add):
                
                profit = profit + (self.stock_add * ohlc_value[4])
                stock_amt -= self.stock_add
                self.transaction.append([ohlc_value[0], ohlc_value[4], 0, profit, stock_amt, ohlc_value[7]])
                            
            else:
                
                profit = profit + (2 * ohlc_value[4])
                stock_amt -= 2
                self.transaction.append([ohlc_value[0], ohlc_value[4], 0, profit, stock_amt, ohlc_value[7]])
           
        return self.transaction, profit, stock_amt
    
    # Perform trading by looking first at the daily data and then looking at the hourly data if momentum reversal 
    # is detected on daily data
    
    def trading_decision(self):
        
        self.ohlc_daily_hist = []
        self.ohlc_hourly_hist = []
        self.transaction = []
        
        max_stock_amt = 10
    
        stock_amt = 0
        profit = 0

        self.df_daily.reset_index(inplace=True)
        self.df_hourly.reset_index(inplace=True)
        
        self.prev_state_hourly = 0
        self.prev_state_daily = 0
        
                                 
        for i in range (self.rolling_window, len(self.df_daily)):
           
            self.ohlc_daily = DataFeed(self.df_daily.iloc[i], self.ohlc_daily_hist, self.indicators, self.mov_avg_daily).get_values()
            self.indicator_daily = DataFeed(self.df_daily.iloc[i], self.ohlc_daily_hist, self.indicators, self.mov_avg_daily).get_indicators()
            
            
            self.today_hourly_stock = self.df_hourly[self.df_hourly['date'] == self.ohlc_daily[0]]
            self.today_hourly_stock.reset_index(inplace=True)
            
            
            self.current_state_daily = self.state_check(self.indicator_daily, self.indicators)
            
            
            
            if self.current_state_daily != self.prev_state_daily:
                
                for j in range (len(self.today_hourly_stock)):
                    
                    self.ohlc_hourly = DataFeed(self.today_hourly_stock.iloc[j], self.ohlc_hourly_hist, self.indicators, self.mov_avg_hourly).get_values()
                    self.indicator_hourly = DataFeed(self.today_hourly_stock.iloc[j], self.ohlc_hourly_hist, self.indicators, self.mov_avg_hourly).get_indicators()
                    
                    self.current_state_hourly = self.state_check(self.indicator_hourly, self.indicators)
                    
                    stock_left = max_stock_amt - stock_amt
                    
                    
                    if self.current_state_hourly != self.prev_state_hourly:
                        
                        
                        self.transaction, profit, stock_amt = self.trading_rules(self.ohlc_hourly, self.indicator_hourly, self.indicator_daily, self.indicators, stock_left, max_stock_amt, stock_amt, profit, self.transaction)
                    
                    self.prev_state_hourly = self.current_state_hourly


            if i == (len(self.df_daily)-2):
                
                if stock_amt != 0:
            
                    profit = profit + (stock_amt * self.today_hourly_stock['close'].iloc[-1])
                    stock_amt = 0
                    self.transaction.append([self.today_hourly_stock['date'].iloc[-1], self.today_hourly_stock['close'].iloc[-1], 0, profit, stock_amt, self.today_hourly_stock['datetime'].iloc[-1]])
            
            self.prev_state_daily =  self.current_state_daily
           
        profit = self.transaction[-1][3]
        
        return profit, self.transaction

# Candlestick visualization
        
def viz_candlestick(df):
    
    fig = go.Figure(data = [go.Candlestick(x = df['datetime'],
                open = df['open'],
                high = df['high'],
                low = df['low'],
                close = df['close'],
                name = 'OHLC')])

    fig.add_trace(go.Scatter(x = df['datetime'], y=df['vwap'], name = 'VWAP'))
    
    return fig

# MACD visualization
    
def viz_macd(df):
    
    macd = go.Scatter(x = df['datetime'], y = df['macd'], name = 'MACD Line')
    macd_s = go.Scatter(x = df['datetime'], y = df['macds'], name = 'MACD Signal')
    macd_h = go.Bar(x = df['datetime'], y = df['macdh'], name = 'MACD Histogram')
    data = [macd, macd_s, macd_h]
    fig_macd = go.Figure(data = data)
   
    return fig_macd

# RSI visualization

def viz_rsi(df, mov_avg, overbought, oversold):
    
    rsi = go.Scatter(x = df['datetime'], y = df['rsi_'+str(mov_avg)])
    
    data_rsi = [rsi]
    
    fig_rsi = go.Figure(data = data_rsi)
    fig_rsi.add_shape(type = 'line', x0 =df['datetime'][0], y0 = overbought, 
                  x1 = df['date'].iloc[-1], y1= overbought)
    fig_rsi.add_shape(type = 'line', x0 = df['datetime'][0], y0 = oversold, 
                  x1 = df['date'].iloc[-1], y1 = oversold)
    
    return fig_rsi


# Trading visualization
    
def viz_trade_decision(df, net, indicators):
    
    net_df = pd.DataFrame(np.array(net), columns = ['date', 'close', 'status', 'profit', 'stock', 'datetime'])

    net_df['datetime'] = pd.to_datetime(net_df['datetime'])
    

    def SetColor(x):
    
        if(x == 1):
            return "red"
        elif(x == 0):
            return "green"

    color = list(map(SetColor, net_df['status']))
    
    net_df['color'] = color
    
    net_df_buy = net_df[net_df['status'] == 1]
    net_df_sell = net_df[net_df['status'] == 0]

    data_points = go.Scatter(
                    x = df['datetime'], 
                    y = df['close'],
                    name = 'Close Price',
                    mode = 'lines'
                    )
    
    buy_points = go.Scatter(
                    x = net_df_buy['datetime'], 
                    y = net_df_buy['close'],
                    customdata = np.dstack((net_df_buy['stock'], net_df_buy['profit'])),
                    name = 'Buy',
                    mode = 'markers',
                    text = ['Datetime: %s<br>Stock: %d<br>Profit: $%d'%(d,t,s) for d,t,s in net_df_buy.loc[:,['datetime','stock','profit']].values],
                    marker = dict(color = net_df_buy['color']) 
                    )  

    sell_points = go.Scatter(
                    x = net_df_sell['datetime'], 
                    y = net_df_sell['close'],
                    name = 'Sell',
                    mode = 'markers',
                    text = ['Datetime: %s<br>Stock: %d<br>Profit: $%d'%(d,t,s) for d,t,s in net_df_sell.loc[:,['datetime','stock','profit']].values],
                    marker = dict(color = net_df_sell['color']))
    
    if indicators == 'bb':
        
        upper_points = go.Scatter(
                    x = df['datetime'], 
                    y = df['upper_band'],
                    name = 'Upper Bands',
                    mode = 'lines',
                    opacity = 0.4
                    )
        
        lower_points = go.Scatter(
                    x = df['datetime'], 
                    y = df['lower_band'],
                    name = 'Lower Bands',
                    mode = 'lines',
                    opacity = 0.4
                    )
        
        data = [data_points, buy_points, sell_points, upper_points, lower_points]
        
    else:
        
        data = [data_points, buy_points, sell_points]
    
    fig = go.Figure(data = data)
    
    return fig








