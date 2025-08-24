import pandas as pd
from strategy import MovingAverageStrategy
from backtest import Backtest
from risk_manager import RiskManager

def main():
    strategy = MovingAverageStrategy()
    data = strategy.generate_signals()

    rm = RiskManager(max_position=0.1)
    data["Position"] = data["Signal"].apply(lambda x: rm.apply_risk(x))

    data["Returns"] = data["Close"].pct_change() * data["Position"]
    data["PortfolioValue"] = (1 + data["Returns"].fillna(0)).cumprod() * 100000

    print(data.tail())

    bt = Backtest(data)
    bt.plot_results()

if __name__ == "__main__":
    main()

