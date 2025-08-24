import pandas as pd

class Portfolio:
    def __init__(self, initial_capital=100000):
        self.cash = initial_capital
        self.history = {}  
        self.total_portfolio = pd.DataFrame() 

    def calculate(self, data_dict, risk_manager):
        """
        data_dict: dict of {symbol: DataFrame}
        """
        self.total_portfolio = pd.DataFrame()
        total_capital = self.cash

        for symbol, data in data_dict.items():
            data = data.copy()
            data["position"] = data["signal"].apply(lambda x: risk_manager.apply_risk(x))
            data["returns"] = data["close"].pct_change() * data["position"]
            asset_capital = total_capital / len(data_dict)
            data["portfoliovalue"] = (1 + data["returns"].fillna(0)).cumprod() * asset_capital
            self.history[symbol] = data

        combined = pd.concat([df["portfoliovalue"] for df in self.history.values()], axis=1)
        combined.columns = list(self.history.keys())
        combined["total_portfolio"] = combined.sum(axis=1)
        self.total_portfolio = combined

        return self.history, self.total_portfolio

