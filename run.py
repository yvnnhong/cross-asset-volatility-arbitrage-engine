import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from src.data_loader import load_data
from src.volatility import realized_vol
from src.signals import calculate_spread, generate_signals
from src.optimizer import optimize_portfolio
from src.backtest import backtest
import os

def plot_results(z_score, signals, backtest_results, prices):
    """Generate plots for z-score, signals, and performance."""
    os.makedirs('visualizations', exist_ok=True)
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(12, 10), sharex=True)
    
    # Z-score and signals
    ax1.plot(z_score, label='Z-score')
    ax1.axhline(1.5, color='r', linestyle='--', alpha=0.5)
    ax1.axhline(-1.5, color='r', linestyle='--', alpha=0.5)
    ax1.axhline(0, color='k', linestyle='-', alpha=0.5)
    ax1.set_title('Volatility Spread Z-score')
    ax1.legend()
    
    # Trade signals
    long_signals = signals[signals == 1].index
    short_signals = signals[signals == -1].index
    ax2.plot(prices.index, prices['GLD'], label='GLD')
    ax2.plot(prices.index, prices['GDX'], label='GDX')
    ax2.scatter(long_signals, prices.loc[long_signals, 'GLD'], c='g', marker='^', label='Long GLD')
    ax2.scatter(short_signals, prices.loc[short_signals, 'GLD'], c='r', marker='v', label='Short GLD')
    ax2.set_title('Trade Signals')
    ax2.legend()
    
    # Cumulative PnL
    ax3.plot(backtest_results['cumulative_pnl'], label='Strategy PnL')
    ax3.set_title(f"Cumulative PnL (Sharpe: {backtest_results['sharpe']:.2f}, Max DD: {backtest_results['max_drawdown']:.2%})")
    ax3.legend()
    
    plt.tight_layout()
    plt.savefig('visualizations/backtest_results.png')
    plt.close()

def main():
    """Run the full volatility arbitrage pipeline."""
    # Configuration
    tickers = ['GLD', 'GDX']
    start_date = "2015-01-01"
    
    # Load data
    prices = load_data(tickers, start_date)
    if prices is None:
        print("Failed to load data. Exiting.")
        return
    
    # Calculate volatility
    vol_gld = realized_vol(prices['GLD'])
    vol_gdx = realized_vol(prices['GDX'])
    
    # Calculate spread and signals
    z_score = calculate_spread(vol_gld, vol_gdx)
    signals = generate_signals(z_score)
    
    # Optimize portfolio
    returns = prices.pct_change().dropna()
    weights = optimize_portfolio(returns, signals)
    
    # Run backtest
    backtest_results = backtest(prices, signals, weights)
    
    # Visualize results
    plot_results(z_score, signals, backtest_results, prices)
    
    # Save performance summary
    summary = {
        'Sharpe Ratio': backtest_results['sharpe'],
        'Max Drawdown': backtest_results['max_drawdown'],
        'Total Return': backtest_results['cumulative_pnl'][-1]
    }
    pd.Series(summary).to_csv('data/performance_summary.csv')
    print("Backtest complete. Results saved to visualizations/ and data/")

if __name__ == "__main__":
    main()