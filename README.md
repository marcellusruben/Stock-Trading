# Stock Trading with Combinations of Technical Indicators (MACD - RSI - VWAP)

## Objective
The purpose of this project is to create a framework that automates the trading process given the particular stock data.
The stock trading algorithm is built based on the combinations of two technical indicators: a momentum indicator and a trend indicator.
There are two momentum indicators that the user can choose, which are the Moving Average Convergence Divergence (MACD) and the Relative Strength Index (RSI). The one trend indicator that is implemented in this project is the Volume Weighted Average Price (VWAP). The trading algorithm utilizes the combinations of either MACD or RSI and VWAP, depending on user's preference.

To visualize the trading result, a web app manager using Streamlit is implemented. There are three different visualization presented in the web app, which are: the candlestick chart, the technical indicator chart (MACD or RSI), and the trading decision chart.

Below is the example of each of these three visualization:

## Candlestick Chart
Candlestick chart represents the open, close, high, and low price of a stock in any given time period.
<p align="center">
  <img width="700" height="350" src=https://github.com/marcellusruben/Image_Cartooning_Web_App/blob/master/image/pencil_edges.png>
</p>

## Technical Indicator Chart
There two momentum indicators that the user can choose from: MACD or RSI.


## Trading Decision Chart
Trading decision chart shows each point in time where the user is recommended to make a trade of their stocks (buy or sell) to gain as much profit as possible.


Below is the example of the web app of this stock trading framework:


## Files
There are four Python files and three text files in this project:

- generate_file.py: a Python file to generate a minutely stock data into other time-frame (available options are: 10 minutely, hourly, daily, and weekly)
- func.py: a Python file that contains necessary classes and functions to conduct a stock trading algorithm.
- InputParam.txt: a text file that contains the user input.
- H_AAPL.txt: Apple hourly stock data.
- D_AAPL.txt: Apple daily stock data.
- main.py: a main Python file to execute all the user command from InputParam.txt and making a stock trading decision.
- app.py: a Python file to execute the web app for this stock trading project.

To execute the web app, go to the working directory of the app.py and type the following command in the conda environment:
```
streamlit run app.py
```
