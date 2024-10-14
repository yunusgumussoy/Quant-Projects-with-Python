# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 22:16:07 2024

@author: Yunus
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tbats import TBATS
import yfinance as yf
from sklearn.metrics import mean_absolute_error
from statsmodels.tsa.stattools import adfuller

# Function to check stationarity
def check_stationarity(data):
    result = adfuller(data)
    return result[1] <= 0.05  # p-value

# Download Bitcoin data
btc_data = yf.download('BTC-USD', start='2020-01-01', end='2024-01-01', interval='1d')

# Extract the 'Close' price
btc_close = btc_data['Close'].dropna()

# Ensure 'Close' is numeric
btc_close = pd.to_numeric(btc_close, errors='coerce')

# Create a DataFrame for feature engineering
btc_close = pd.DataFrame(btc_close)

# Feature Engineering
btc_close['Lag1'] = btc_close['Close'].shift(1)
btc_close['Lag7'] = btc_close['Close'].shift(7)
btc_close['MA7'] = btc_close['Close'].rolling(window=7).mean()
btc_close['MA30'] = btc_close['Close'].rolling(window=30).mean()
btc_close['Returns'] = btc_close['Close'].pct_change()

# Drop NaN values from new features
btc_close = btc_close.dropna()

# Check stationarity
if not check_stationarity(btc_close['Close']):
    print("Data is not stationary. Consider differencing or transformations.")

# Splitting the data into training and testing sets
train_size = int(len(btc_close) * 0.8)
train, test = btc_close[:train_size], btc_close[train_size:]

# Fit the TBATS model on training data
tbats_model = TBATS(seasonal_periods=[7])
tbats_fitted = tbats_model.fit(train['Close'])

# Forecasting
forecast = tbats_fitted.forecast(steps=len(test))

# Evaluate the model
mae = mean_absolute_error(test['Close'], forecast)
print(f'Mean Absolute Error: {mae}')

# Plotting
plt.figure(figsize=(12, 6))
plt.plot(train['Close'], label='Training Data', color='orange')
plt.plot(test['Close'].index, test['Close'], label='Test Data', color='green')
plt.plot(test['Close'].index, forecast, label='TBATS Forecast', color='blue', linestyle='--')
plt.title('Bitcoin Price Forecast with Improvements')
plt.xlabel('Date')
plt.ylabel('Price (USD)')
plt.legend()
plt.show()
