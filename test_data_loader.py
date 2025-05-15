from src.data_loader import load_data

tickers = ['GLD', 'GDX']
prices = load_data(tickers, start_date="2015-01-01")
if prices is not None:
    print("Data loaded successfully:")
    print(prices.head())
else:
    print("Failed to load data")