# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 15:56:12 2024

@author: Yunus
"""



import yfinance as yf
import statsmodels.api as sm
import pandas as pd

# Download stock and market data (S&P 500 as proxy for market)
stock_data = yf.download('AAPL', start='2018-01-01', end='2025-01-01')['Adj Close']
market_data = yf.download('^GSPC', start='2018-01-01', end='2025-01-01')['Adj Close']

# Calculate returns
stock_returns = stock_data.pct_change()
market_returns = market_data.pct_change()

# Risk-free rate (proxy: 3-month Treasury bill)
rf = yf.download('^IRX', start='2018-01-01', end='2025-01-01')['Adj Close'] / 100
rf = rf.resample('D').ffill()  # Forward fill to fill in gaps (e.g., weekends)
rf_returns = rf.pct_change()

# Combine all data into a DataFrame
data = pd.DataFrame({
    'stock_returns': stock_returns,
    'market_returns': market_returns,
    'rf_returns': rf_returns
})

# Drop rows with any missing data (NaN or inf)
data = data.dropna()

# Calculate excess returns
data['excess_stock'] = data['stock_returns'] - data['rf_returns']
data['excess_market'] = data['market_returns'] - data['rf_returns']

# CAPM regression
X = sm.add_constant(data['excess_market'])
y = data['excess_stock']
model = sm.OLS(y, X)
results = model.fit()
print(results.summary())
