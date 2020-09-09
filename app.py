# -*- coding: utf-8 -*-

import pandas as pd
import numpy as np
from stockstats import StockDataFrame as sdf
import plotly.graph_objs as go
import streamlit as st
import func as f
import datetime

######################## USER INPUT PARAMETERS ################################

filename_daily = st.sidebar.text_input('Enter the filename of daily stock', 'D_AAPL.txt')
filename_hourly = st.sidebar.text_input('Enter the filename of hourly stock', 'H_AAPL.txt')

time_begin = st.sidebar.date_input('Start date', datetime.date(2020, 1, 1), min_value = datetime.date(2000, 1, 1), max_value = datetime.date(2020, 7, 1))
time_end = st.sidebar.date_input('End date', datetime.date(2020, 6, 1), min_value = datetime.date(2000, 1, 1), max_value = datetime.date(2020, 7, 1))

if time_begin < time_end:
    st.success('Start date: `%s`\n\nEnd date:`%s`' % (time_begin, time_end))
else:
    st.error('Error: End date must fall after start date.')


trading_style = st.sidebar.selectbox('Choose your trading style:', ('Risk Taking', 'Risk Averse'))

if trading_style == 'Risk Taking':
    
    stock_add = 8

elif trading_style == 'Risk Averse':
    
    stock_add = 4

option_ind = st.sidebar.selectbox('Choose a momentum indicator:', ('MACD', 'RSI', 'Bollinger Bands'))

if option_ind == 'MACD':
    
    indicators = 'macd'
    
elif option_ind == 'RSI':
    
    indicators = 'rsi'

elif option_ind == 'Bollinger Bands':
    
    indicators = 'bb'

if indicators == 'rsi':
    
    overbought = st.sidebar.slider('Overbought Threshold', 50, 90, 80)
    oversold = st.sidebar.slider('Oversold Threshold', 10, 50, 20)
    rsi_mov_avg_hourly = st.sidebar.slider('Hourly RSI Moving Average', 1, 200, 14)
    rsi_mov_avg_daily = st.sidebar.slider('Daily RSI Moving Average', 1, 200, 7)

else:
    
    rsi_mov_avg_hourly = None
    rsi_mov_avg_daily = None
    overbought = None
    oversold = None

vwap_window_hourly = st.sidebar.slider('Hourly VWAP Moving Average', 1, 200, 105)
vwap_window_daily = st.sidebar.slider('Daily VWAP Moving Average', 1, 200, 15)

######################## READ FILES ###########################################

df_daily = f.file_reading(filename_daily, vwap_window_daily, time_begin, time_end, indicators, rsi_mov_avg_daily)
df_hourly = f.file_reading(filename_hourly, vwap_window_hourly, time_begin, time_end, indicators, rsi_mov_avg_hourly) 

df_daily.reset_index(inplace=True)
df_hourly.reset_index(inplace=True)

########################## PERFORM TRADING ####################################
profit, net = f.Trader(df_hourly, df_daily, indicators, rsi_mov_avg_daily, rsi_mov_avg_hourly , overbought, oversold, vwap_window_daily, stock_add).trading_decision()
profit_regular = (10*df_hourly['close'].iloc[-1]) - (10*df_hourly['close'].iloc[0])

######################## MAIN PAGE ############################################

st.title('Stock Trading with MACD / RSI and VWAP Indicators')

'''
With this app, stock trading using momentum indicators like MACD and RSI
can be performed. Specifically, one of these two momentum indicators will be 
combined with a trend indicator like Volume Weighted Average Price (VWAP) to
make a trading decision at any point of time.

Below you can choose which timeframe of visualizations that you want to display.
On the left hand side, there are several user input parameters that you can choose
like selected time periods, indicator to use, etc.

On the main page below, there are three visualizations: candlestick chart, indicator chart,
and trading decision chart. All of these visualizations are going to change interactively as you change
the user parameters like the time periods.

Finally, below the trading decision chart, you can find the total profit using the trading algorithm and
the profit using the keep-and-sell method. The detailed method behind the trading algorithm applied in this app
can be found in the report.
'''

option_time = st.selectbox( 'Timeframe of the visualization:', ('Daily', 'Hourly'))

if option_time == 'Daily':
    
    df_selected = df_daily
    
elif option_time == 'Hourly':
    
    df_selected = df_hourly
    
########################## CANDLESTICK CHART ############################################


fig = f.viz_candlestick(df_selected)
st.header('Candlestick chart for the selected time periods')
st.plotly_chart(fig)

#########################  MACD CHART #########################################

if indicators == 'macd':
    
    fig_macd = f.viz_macd(df_selected)
    st.header('MACD indicator for the selected time periods')
    st.plotly_chart(fig_macd)
    
######################### RSI CHART ###########################################
    
if indicators == 'rsi':
    
    if option_time == 'Daily':
        
        rsi_mov_avg = rsi_mov_avg_daily
    
    elif option_time == 'Hourly':
        
        rsi_mov_avg = rsi_mov_avg_hourly
        
    fig_rsi = f.viz_rsi(df_selected, rsi_mov_avg, overbought, oversold)
    
    st.header('RSI indicator for the selected time periods')
    
    st.plotly_chart(fig_rsi)
    
###################### TRADE DECISION CHART ###################################
    
fig_decision = f.viz_trade_decision(df_hourly, net, indicators)

st.header('Trading decision for the selected time periods using selected indicator')
'''
Hover around each trading points to see the detail about the trading time, the amount of stocks,
and the profit.
'''
st.plotly_chart(fig_decision)

###############################################################################

st.write('Profit using trading algorithm: $'+str(round(profit,3)))
st.write('Profit using keep and sell strategy: $'+str(round(profit_regular,3)))