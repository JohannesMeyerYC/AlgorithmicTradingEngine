import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os

def plot_portfolio(data, title="Portfolio Backtest", save_as=None, window=20):
    """
    Enhanced portfolio plot with:
    - Close price
    - SMA20, SMA50
    - Portfolio value
    - Buy/sell markers
    - Cumulative returns
    - Drawdowns
    - Rolling Sharpe ratio
    """
    plt.figure(figsize=(14, 8))

    ax1 = plt.gca()
    if 'close' in data.columns:
        ax1.plot(data['close'], label="Close Price", color='blue', alpha=0.7)
    if 'sma20' in data.columns:
        ax1.plot(data['sma20'], label="SMA20", color='orange', linestyle='--')
    if 'sma50' in data.columns:
        ax1.plot(data['sma50'], label="SMA50", color='green', linestyle='--')
    if 'portfoliovalue' in data.columns:
        ax1.plot(data['portfoliovalue'], label="Portfolio Value", color='black', linewidth=2)

    if 'signal' in data.columns:
        buys = data[data['signal'] > 0]
        sells = data[data['signal'] < 0]
        ax1.scatter(buys.index, data.loc[buys.index, 'close'], marker='^', color='green', s=100, label='Buy Signal')
        ax1.scatter(sells.index, data.loc[sells.index, 'close'], marker='v', color='red', s=100, label='Sell Signal')

    ax1.set_ylabel("Price / Portfolio Value")
    ax1.legend(loc='upper left')
    ax1.grid(True)

    if 'portfoliovalue' in data.columns:
        cummax = data['portfoliovalue'].cummax()
        drawdown = (data['portfoliovalue'] - cummax) / cummax
        ax2 = ax1.twinx()
        ax2.fill_between(drawdown.index, drawdown, 0, color='red', alpha=0.2, label='Drawdown')
        ax2.set_ylabel("Drawdown")
        ax2.legend(loc='lower left')

    if 'returns' in data.columns:
        rolling_sharpe = data['returns'].rolling(window).mean() / data['returns'].rolling(window).std() * np.sqrt(252)
        ax3 = ax1.twinx()
        ax3.spines['right'].set_position(('outward', 60))  # offset axis
        ax3.plot(rolling_sharpe, color='purple', label=f'Rolling {window}-day Sharpe')
        ax3.set_ylabel("Rolling Sharpe")
        ax3.legend(loc='upper right')

    plt.title(title)
    plt.tight_layout()

    if save_as:
        os.makedirs("tests", exist_ok=True)
        path = os.path.join("tests", save_as)
        plt.savefig(path)
        print(f"Saved plot to {path}")

    plt.close()


def sharpe_ratio(returns, risk_free=0.0):
    mean = returns.mean()
    std = returns.std()
    if std == 0:
        return 0
    return (mean - risk_free) / std * np.sqrt(252)  # annualized

def cumulative_returns(returns):
    """Calculate cumulative returns from a series of daily returns"""
    return (1 + returns.fillna(0)).cumprod()

def max_drawdown(returns):
    """Compute maximum drawdown"""
    cumulative = cumulative_returns(returns)
    peak = cumulative.cummax()
    drawdown = (cumulative - peak) / peak
    return drawdown.min()

def annualized_volatility(returns):
    """Compute annualized volatility of daily returns"""
    return returns.std() * np.sqrt(252)

def rolling_sharpe(returns, window=252):
    """Compute rolling Sharpe ratio over a window (default 1 year)"""
    return (returns.rolling(window).mean() / returns.rolling(window).std()) * np.sqrt(252)

def summary_stats(returns):
    """Return a summary dict of key portfolio metrics"""
    return {
        "Sharpe Ratio": sharpe_ratio(returns),
        "Max Drawdown": max_drawdown(returns),
        "Annualized Volatility": annualized_volatility(returns),
        "Cumulative Return": cumulative_returns(returns).iloc[-1] - 1
    }
