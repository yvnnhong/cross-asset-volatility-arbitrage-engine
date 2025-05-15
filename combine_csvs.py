import pandas as pd
import os
     
# Ensure data directory exists
os.makedirs('data', exist_ok=True)
     
# Load GLD and GDX CSVs
gld_df = pd.read_csv('data/GLD.csv')
gdx_df = pd.read_csv('data/GDX.csv')
     
# Select Date and Adj Close columns
gld_df = gld_df[['Date', 'Adj Close']].rename(columns={'Adj Close': 'GLD'})
gdx_df = gdx_df[['Date', 'Adj Close']].rename(columns={'Adj Close': 'GDX'})
     
# Merge on Date
combined_df = pd.merge(gld_df, gdx_df, on='Date', how='inner')
     
# Ensure Date is in YYYY-MM-DD format
combined_df['Date'] = pd.to_datetime(combined_df['Date']).dt.strftime('%Y-%m-%d')
     
# Save to prices.csv
combined_df.to_csv('data/prices.csv', index=False)
print("Combined data saved to data/prices.csv")