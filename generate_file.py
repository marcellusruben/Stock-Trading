# -*- coding: utf-8 -*-

import warnings
warnings.simplefilter(action='ignore', category=RuntimeWarning)
import pandas as pd
import numpy as np
import os 


def vwap(df):
    
    # Formula for VWAP
    
    cum_vol = df['Volume'].sum()
    cum_vol_price= (df['Volume'] * (df['High'] + df['Low'] + df['Close']) /3).sum()
    
    return (cum_vol_price/cum_vol)

def generate_file (file_path, time_period):
    
    # Read csv or txt file
    file = os.path.basename(file_path)
    df = pd.read_csv(file_path)
    
    # Convert date and time columns to datetime format

    df['Time'] = (pd.to_datetime(df['Time'],format='%H%M').dt.time)
    df['Date'] = (pd.to_datetime(df['Date']).dt.date)
    df['Datetime'] = pd.to_datetime(df["Date"].astype(str) + " " + df["Time"].astype(str))
    df = df.set_index(['Datetime'])

    #Delete this line if you want to generate the file starting from 1991
    df = df.loc['2019-01-01':'2020-06-01']

    # Calculate the aggregate of vwap
    
    df_vwap = df.groupby(pd.Grouper(freq= time_period)).apply(vwap)
    df_vwap = df_vwap.dropna(how='all')

    # Resample the dataframe according to time period
    
    df_resample = df.resample(time_period).apply({'Date':'first','Open': 'first', 'High': 'max', 'Low': 'min', 'Close': 'last', 'Volume':'sum'})
    df_resample = df_resample[(df_resample != 0).all(1)]

    # Assemble the resampled dataframe with the corresponding vwap value
    
    df_final = pd.concat([df_resample, df_vwap], axis=1)
    df_final.rename(columns = {0:'VWAP'},inplace=True)
    
    # Save the final dataframe
    
    df_final.to_csv(str(time_period)+'_'+str(file))

cwd_path = os.getcwd()

file = input("Please enter the name of the file and its extension: ")
time_period = input("Please enter the time period (10Min, H, D, or W): ")

file_path = os.path.join(cwd_path, file)

try:
    generate_file(file_path, time_period)
except:
    print("Invalid file name or time period")
