import pandas as pd
from strategy import MovingAverageStrategy
from risk_manager import RiskManager
from portfolio import Portfolio
from backtest import Backtest

def main():
    strategy = MovingAverageStrategy()
    data = strategy.generate_signals()

    rm = RiskManager(max_position=0.1)
    pf = Portfolio(initial_capital=100000)
    data = pf.calculate(data, rm)

    print(data.tail())
    Backtest(data).plot_results()

if __name__ == "__main__":
    main()
