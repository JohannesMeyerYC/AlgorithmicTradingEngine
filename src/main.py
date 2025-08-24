import pandas as pd
from risk_manager import RiskManager
from backtest import Backtest
from strategy import MovingAverageStrategy, RSI_MomentumStrategy, MeanReversionStrategy

STRATEGIES = {
    "moving_average": MovingAverageStrategy,
    "rsi": RSI_MomentumStrategy,
    "mean_reversion": MeanReversionStrategy
}

def main(strategy_name="moving_average"):
    StrategyClass = STRATEGIES.get(strategy_name.lower())
    if not StrategyClass:
        raise ValueError(f"Strategy '{strategy_name}' not found. Choose from: {list(STRATEGIES.keys())}")

    symbols = ["AAPL", "MSFT", "GOOG"]  # Add your assets here
    rm = RiskManager(max_position=0.1)
    data_dict = {}

    for symbol in symbols:
        strategy = StrategyClass(symbol=symbol)
        data = strategy.generate_signals()
        data["position"] = data["signal"].apply(lambda x: rm.apply_risk(x))
        data["returns"] = data["close"].pct_change() * data["position"]
        data["portfoliovalue"] = (1 + data["returns"].fillna(0)).cumprod() * 100000
        data_dict[symbol] = data

    # Print the last few rows of each asset
    for symbol, df in data_dict.items():
        print(f"\n=== {symbol} ===")
        print(df.tail())

    Backtest(data_dict).plot_results()



if __name__ == "__main__":
    main(strategy_name="rsi")
