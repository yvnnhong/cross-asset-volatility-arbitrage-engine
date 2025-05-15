import pandas as pd
import numpy as np

def realized_vol(prices, window=21):
    """Calculate annualized realized volatility for given prices."""
    returns = prices.pct_change().dropna()
    return returns.rolling(window).std() * np.sqrt(252)