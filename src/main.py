import pandas as pd
from risk_manager import RiskManager
from backtest import Backtest
from strategy import MovingAverageStrategy, RSI_MomentumStrategy, MeanReversionStrategy
from utils import plot_portfolio, sharpe_ratio


STRATEGIES = {
    "moving_average": MovingAverageStrategy,
    "rsi": RSI_MomentumStrategy,
    "mean_reversion": MeanReversionStrategy
}

def main(strategy_name="moving_average", symbols=None, initial_capital=100000):
    if symbols is None:
        symbols = ["AAPL", "MSFT", "GOOG"]

    StrategyClass = STRATEGIES.get(strategy_name.lower())
    if not StrategyClass:
        raise ValueError(f"Strategy '{strategy_name}' not found. Choose from: {list(STRATEGIES.keys())}")

    rm = RiskManager(max_position=0.1)
    data_dict = {}

    for symbol in symbols:
        strategy = StrategyClass(symbol=symbol)
        data = strategy.generate_signals()
        data["position"] = data["signal"].apply(lambda x: rm.apply_risk(x))
        data["returns"] = data["close"].pct_change() * data["position"]
        data["portfoliovalue"] = (1 + data["returns"].fillna(0)).cumprod() * (initial_capital / len(symbols))
        data_dict[symbol] = data

    for symbol, df in data_dict.items():
        print(f"\n=== {symbol} ===")
        print(df.tail())
        sr = sharpe_ratio(df['returns'].dropna())
        print(f"{symbol} Sharpe Ratio: {sr:.2f}")
        plot_portfolio(df, title=f"{symbol} Backtest", save_as=f"{symbol}_backtest.png")

    portfolio_total = pd.DataFrame(index=data_dict[symbols[0]].index)
    portfolio_total['returns'] = sum(df['returns'] * (1/len(symbols)) for df in data_dict.values())
    portfolio_total['portfoliovalue'] = (1 + portfolio_total['returns'].fillna(0)).cumprod() * initial_capital
    plot_portfolio(portfolio_total, title="Aggregated Portfolio Backtest", save_as="aggregated_portfolio.png")
    sr_total = sharpe_ratio(portfolio_total['returns'])
    print(f"Aggregated Portfolio Sharpe Ratio: {sr_total:.2f}")



if __name__ == "__main__":
    main(strategy_name="rsi")
