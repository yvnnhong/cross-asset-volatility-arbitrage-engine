Cross-Asset Volatility Arbitrage Engine
Overview
This project implements a volatility arbitrage strategy that exploits mispricings in volatility between related asset pairs (e.g., GLD/GDX). It uses historical price data to compute realized volatility, generates trading signals based on z-scores, optimizes portfolio weights using CVXPY, and backtests the strategy with transaction costs. Results are visualized and saved for analysis.
Directory Structure
vol_arbitrage_engine/
│
├── data/               # Cached price data and performance summaries
├── notebooks/          # Exploratory Jupyter notebooks (optional)
├── src/                # Python modules
│   ├── data_loader.py  # Data acquisition
│   ├── volatility.py   # Volatility calculations
│   ├── signals.py      # Signal generation
│   ├── optimizer.py    # Portfolio optimization
│   └── backtest.py     # Backtesting logic
├── visualizations/     # Output plots
├── tests/              # Unit tests (optional)
├── requirements.txt    # Dependencies
├── README.md           # Project documentation
└── run.py              # Main script

Setup

Clone the Repository:
git clone <your-repo-url>
cd vol_arbitrage_engine


Install Dependencies:
pip install -r requirements.txt


Run the Pipeline:
python run.py



Methodology

Data Acquisition: Downloads adjusted close prices for GLD and GDX using yfinance.
Volatility Estimation: Computes 21-day annualized realized volatility.
Signal Generation: Calculates z-score of volatility spread; enters trades when |z-score| > 1.5, exits when z-score crosses 0.
Portfolio Optimization: Uses CVXPY to compute dollar-neutral weights, minimizing risk.
Backtesting: Simulates trades with 5 bps transaction costs; computes Sharpe ratio and max drawdown.
Visualization: Plots z-score, trade signals, and cumulative PnL.

Outputs

Data: data/prices.csv (price data), data/performance_summary.csv (metrics).
Visualizations: visualizations/backtest_results.png (z-score, signals, PnL).

Stretch Goals

Add PyTorch for volatility forecasting.
Implement dynamic hedge ratios via PCA or regression.
Create a Streamlit dashboard.
Dockerize the project.
Store historical data in SQLite.

Requirements

Python 3.10+
See requirements.txt for dependencies.

Usage
Run python run.py to execute the full pipeline. Modify tickers in run.py to test other asset pairs (e.g., SPY/VIX).
Notes

Ensure internet access for yfinance data downloads.
CVXPY may require a compatible solver (e.g., ECOS, SCS).
Add tests in tests/ for production use.

