import pandas as pd
import yfinance as yf
from datetime import datetime
import os

def load_data(tickers, start_date="2015-01-01", end_date=None):
    """Load adjusted close prices for given tickers and cache to CSV."""
    os.makedirs('data', exist_ok=True)
    cache_file = 'data/prices.csv'
    
    # Check if cached data exists
    if os.path.exists(cache_file):
        try:
            df = pd.read_csv(cache_file, index_col=0, parse_dates=True)
            print(f"Loaded cached data from {cache_file}")
            return df
        except Exception as e:
            print(f"Error reading cached data: {e}")
    
    # Fetch data from yfinance
    if end_date is None:
        end_date = datetime.today().strftime('%Y-%m-%d')
    try:
        df = yf.download(tickers, start=start_date, end=end_date, auto_adjust=True)['Close']
        df.to_csv(cache_file)
        print(f"Downloaded data and saved to {cache_file}")
        return df
    except Exception as e:
        print(f"Error loading data from yfinance: {e}")
        return None