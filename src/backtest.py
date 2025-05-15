import pandas as pd
import numpy as np

def backtest(prices, signals, weights, transaction_cost_bps=5):
    """Backtest the strategy with transaction costs and compute performance metrics."""
    returns = prices.pct_change().dropna()
    portfolio_returns = (returns * weights.shift(1)).sum(axis=1)
    
    # Apply transaction costs
    weight_changes = weights.diff().abs().sum(axis=1)
    transaction_costs = weight_changes * (transaction_cost_bps / 10000)
    portfolio_returns -= transaction_costs
    
    # Performance metrics
    cumulative_pnl = (1 + portfolio_returns).cumprod() - 1
    sharpe = portfolio_returns.mean() / portfolio_returns.std() * np.sqrt(252) if portfolio_returns.std() != 0 else 0
    max_drawdown = (cumulative_pnl.cummax() - cumulative_pnl).max()
    
    return {
        'returns': portfolio_returns,
        'cumulative_pnl': cumulative_pnl,
        'sharpe': sharpe,
        'max_drawdown': max_drawdown
    }