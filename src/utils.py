import matplotlib.pyplot as plt
import pandas as pd

def plot_portfolio(data, title="Portfolio Backtest"):
    plt.figure(figsize=(12, 6))
    if 'close' in data.columns:
        plt.plot(data['close'], label="Close Price")
    if 'sma20' in data.columns:
        plt.plot(data['sma20'], label="SMA20")
    if 'sma50' in data.columns:
        plt.plot(data['sma50'], label="SMA50")
    if 'PortfolioValue' in data.columns:
        plt.plot(data['PortfolioValue'], label="Portfolio Value")
    plt.legend()
    plt.title(title)
    plt.show()

def sharpe_ratio(returns, risk_free=0.0):
    mean = returns.mean()
    std = returns.std()
    if std == 0:
        return 0
    return (mean - risk_free) / std * (252 ** 0.5)  # annualized
