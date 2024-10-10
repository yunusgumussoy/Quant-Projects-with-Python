# -*- coding: utf-8 -*-
"""
Created on Sun Sep 29 16:09:14 2024

@author: Yunus
"""

import yfinance as yf
import pandas as pd
import statsmodels.api as sm

# Download stock price data (Apple)
stock_data = yf.download('AAPL', start='2018-01-01', end='2025-01-01')['Adj Close']

# Download S&P 500 (market) data
market_data = yf.download('^GSPC', start='2018-01-01', end='2025-01-01')['Adj Close']

# Download Treasury yield (10-year yield from FRED)
treasury_data = yf.download('^TNX', start='2018-01-01', end='2025-01-01')['Adj Close']

# Download oil price data (WTI crude oil prices)
oil_data = yf.download('CL=F', start='2018-01-01', end='2025-01-01')['Adj Close']

# Calculate daily stock returns
stock_returns = stock_data.pct_change().dropna()

# Calculate daily market returns (S&P 500)
market_returns = market_data.pct_change().dropna()

# Calculate daily changes in Treasury yield
treasury_rate_change = treasury_data.pct_change().dropna()

# Calculate daily changes in oil prices
oil_returns = oil_data.pct_change().dropna()

# Align all data by date
data = pd.concat([stock_returns, market_returns, treasury_rate_change, oil_returns], axis=1).dropna()
data.columns = ['Stock_Return', 'Market_Return', 'Treasury_Yield_Change', 'Oil_Return']

# Define excess returns for the stock and market (assuming no risk-free rate for simplicity here)
excess_stock = data['Stock_Return']
excess_market = data['Market_Return']

# Create the factor matrix (Market, Treasury Rate, Oil)
factors = data[['Market_Return', 'Treasury_Yield_Change', 'Oil_Return']]

# Add a constant for the intercept
factors = sm.add_constant(factors)

# Run the APT regression (OLS)
model = sm.OLS(excess_stock, factors)
results = model.fit()

# Output regression results
print(results.summary())
