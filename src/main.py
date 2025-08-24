import pandas as pd
from risk_manager import RiskManager
from backtest import Backtest
from strategy import MovingAverageStrategy, RSI_MomentumStrategy, MeanReversionStrategy
from utils import plot_portfolio, sharpe_ratio, CostModel  


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
    cost_model = CostModel(fixed_fee=1, proportional_fee=0.001, slippage=0.0005)
    data_dict = {}

    for symbol in symbols:
        strategy = StrategyClass(symbol=symbol)
        data = strategy.generate_signals()
        data["position"] = data["signal"].apply(lambda x: rm.apply_risk(x))
        data["returns"] = data["close"].pct_change() * data["position"]

        data["position_change"] = data["position"].diff().fillna(data["position"])
        data["transaction_cost"] = data.apply(
            lambda row: cost_model.apply_cost(row["close"], row["position_change"]),
            axis=1
        )

        asset_capital = initial_capital / len(symbols)
        data["returns_net"] = data["returns"] - data["transaction_cost"] / asset_capital
        data["portfoliovalue"] = (1 + data["returns_net"].fillna(0)).cumprod() * asset_capital

        data_dict[symbol] = data

    for symbol, df in data_dict.items():
        print(f"\n=== {symbol} ===")
        print(df.tail())
        sr = sharpe_ratio(df['returns_net'].dropna())
        print(f"{symbol} Sharpe Ratio: {sr:.2f}")
        plot_portfolio(df, title=f"{symbol} Backtest", save_as=f"{symbol}_backtest.png")

    portfolio_total = pd.DataFrame(index=data_dict[symbols[0]].index)
    portfolio_total['returns'] = sum(df['returns_net'] * (1/len(symbols)) for df in data_dict.values())
    portfolio_total['portfoliovalue'] = (1 + portfolio_total['returns'].fillna(0)).cumprod() * initial_capital
    plot_portfolio(portfolio_total, title="Aggregated Portfolio Backtest", save_as="aggregated_portfolio.png")
    sr_total = sharpe_ratio(portfolio_total['returns'])
    print(f"Aggregated Portfolio Sharpe Ratio: {sr_total:.2f}")



if __name__ == "__main__":
    main(strategy_name="rsi")
