import pandas as pd

class Portfolio:
    def __init__(self, initial_capital=100000):
        self.cash = initial_capital
        self.positions = {}
        self.history = {}


    def calculate(self, data_dict, risk_manager):
        for symbol, data in data_dict.items():
            data = data.copy()
            data["position"] = data["signal"].apply(lambda x: risk_manager.apply_risk(x))
            data["returns"] = data["close"].pct_change() * data["position"]
            data["portfoliovalue"] = (1 + data["returns"].fillna(0)).cumprod() * self.cash
            self.history[symbol] = data
        return data
