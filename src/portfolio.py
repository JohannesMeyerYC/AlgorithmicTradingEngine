import pandas as pd

class Portfolio:
    def __init__(self, initial_capital=100000):
        self.initial_capital = initial_capital

    def calculate(self, data, risk_manager):
        data["position"] = data["signal"].apply(lambda x: risk_manager.apply_risk(x))
        data["returns"] = data["close"].pct_change() * data["position"]
        data["portfoliovalue"] = (1 + data["returns"].fillna(0)).cumprod() * self.initial_capital
        return data
