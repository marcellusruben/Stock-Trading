# -*- coding: utf-8 -*-

import numpy as np
import pandas as pd
import os
from datetime import datetime
import plotly.graph_objs as go
import plotly.io as pio
pio.renderers.default = "browser"
import func as f

##################### GET WORKING DIRECTORY ###################################
filepath = os.getcwd()

################ PROCESS USER INPUT PARAMETERS ################################
p = f.UserParameters()
p.read_file(filepath)

########################## READ FILES #########################################
#print(p.rsi_mov_avg_daily)14
df_daily = f.file_reading(p.filename_daily, p.vwap_window_daily, p.time_begin, p.time_end, p.indicator, p.rsi_mov_avg_daily)
df_hourly = f.file_reading(p.filename_hourly, p.vwap_window_hourly, p.time_begin, p.time_end, p.indicator, p.rsi_mov_avg_hourly)

df_daily.reset_index(inplace=True)
df_hourly.reset_index(inplace=True)


########################## PERFORM TRADING ####################################
profit, net = f.Trader(df_hourly, df_daily, p.indicator, p.rsi_mov_avg_daily, p.rsi_mov_avg_hourly, p.overbought, p.oversold, p.vwap_window_daily, p.stock_add).trading_decision()
profit_regular = (10*df_hourly['close'].iloc[-1]) - (10*df_hourly['close'].iloc[0])

print('Profit using trading algorithm: $'+str(profit))
print('Profit using keep and sell strategy: $'+str(profit_regular))

if p.option_time == 'daily':
    
    df_selected = df_daily

elif p.option_time == 'hourly':
    
    df_selected = df_hourly
    
########################## CANDLESTICK CHART ##################################  
fig = f.viz_candlestick(df_selected)
fig.update_layout(title={
        'text': "Candlestick Chart",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig.show()


###################### MOMENTUM INDICATOR CHART ###############################
if p.indicator == 'macd':
    
    fig_macd = f.viz_macd(df_selected)
    fig_macd.update_layout(title={
        'text': "MACD Indicator",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig_macd.show()

elif p.indicator == 'rsi':
    
    if p.option_time == 'daily':
        rsi_mov_avg = p.rsi_mov_avg_daily
    
    elif p.option_time == 'hourly':
        rsi_mov_avg = p.rsi_mov_avg_hourly
        
    fig_rsi = f.viz_rsi(df_selected, rsi_mov_avg, p.overbought, p.oversold)
    fig_rsi.update_layout(title={
        'text': "RSI Indicator",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
    fig_rsi.show()

##################### TRADE DECISION CHART ##################################
fig_decision = f.viz_trade_decision(df_hourly, net, p.indicator)
fig_decision.update_layout(title={
        'text': "Trade Decision",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'})
fig_decision.show()



