# -*- coding: utf-8 -*-
"""
Created on Tue Oct  1 15:57:53 2024

@author: Yunus
"""

import ccxt
import pandas as pd
from datetime import datetime, timedelta
import time

exchange = ccxt.binance()

top_100_symbols = list(set([
    'BTC', 'ETH', 'SOL', 'BNB', 'XRP', 'ADA', 'DOGE', 'DOT', 'UNI', 'LTC',
    'LINK', 'BCH', 'MATIC', 'ALGO', 'VET', 'XLM', 'ATOM', 'AVAX', 'FTT', 'TRX',
    'SHIB', 'ETC', 'FIL', 'XMR', 'THETA', 'EOS', 'AAVE', 'KSM', 'NEO', 'XTZ',
    'MKR', 'DASH', 'ZIL', 'COMP', 'YFI', 'RUNE', 'SNX', 'ENJ', 'BAT', 'MANA',
    'GRT', '1INCH', 'SUSHI', 'CELO', 'ZRX', 'WAVES', 'OMG', 'ONT', 'QTUM',
    'BTT', 'CHZ', 'IOST', 'ICX', 'ZEN', 'SC', 'UMA', 'KNC', 'BAL', 'BAND',
    'ANKR', 'DGB', 'HNT', 'OCEAN', 'RSR', 'ZEC', 'KLAY', 'CKB', 'ASTR', 'BNX',
    'LUNA', 'FTM', 'HBAR', 'ICP', 'KDA', 'QNT', 'FLOW', 'AXS', 'NEAR', 'RAY',
    'DODO', 'PUNDIX', 'TOMO', 'XEM', 'HOT', 'STMX', 'IOTX', 'LPT', 'SXP',
    'PLA', 'AKRO', 'BZRX', 'STORJ', 'OXT', 'MITH', 'KAVA', 'ROSE', 'CHR', 'CTK'
]))

def fetch_ohlcv(symbol, since):
    market_symbol = f"{symbol}/USDT"
    all_ohlcv = []
    while True:
        try:
            ohlcv = exchange.fetch_ohlcv(market_symbol, timeframe='1d', since=since, limit=1000)
            if not ohlcv:
                break
            since = ohlcv[-1][0] + 86400000  # Move to the next day
            all_ohlcv.extend(ohlcv)
            
            if len(ohlcv) < 1000:
                break
        except Exception as e:
            print(f"Error fetching data for {market_symbol}: {e}")
            time.sleep(5)  # Delay before retry
            continue
 
    df = pd.DataFrame(all_ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
    df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
    df['symbol'] = symbol
    return df

all_data = pd.DataFrame()

# Define the start date
start_date = '2010-01-01'
since_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp() * 1000)

for symbol in top_100_symbols:
    print(f"Fetching data for {symbol}...")
    df = fetch_ohlcv(symbol, since_timestamp)
    all_data = pd.concat([all_data, df], ignore_index=True)


output_path = 'crypto_data.csv'
all_data.to_csv(output_path, index=False)


print(f"Data collection process completed at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Data has been saved to the file: {output_path}")