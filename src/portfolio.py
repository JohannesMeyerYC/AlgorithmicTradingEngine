import pandas as pd
from utils import CostModel

class Portfolio:
    def __init__(self, initial_capital=100000, cost_model=None):
        self.cash = initial_capital
        self.history = {}  
        self.total_portfolio = pd.DataFrame() 
        self.cost_model = cost_model

    def calculate(self, data_dict, risk_manager):
    """
    data_dict: dict of {symbol: DataFrame}
    """
    self.total_portfolio = pd.DataFrame()
    total_capital = self.cash

    for symbol, data in data_dict.items():
        data = data.copy()
        data["position"] = data["signal"].apply(lambda x: risk_manager.apply_risk(x))

        # Calculate position changes (shares or fraction)
        data["position_change"] = data["position"].diff().fillna(data["position"])

        # Base returns
        data["returns"] = data["close"].pct_change() * data["position"]

        # Apply transaction costs if a cost model is provided
        if self.cost_model:
            data["transaction_cost"] = data.apply(
                lambda row: self.cost_model.apply_cost(row["close"], row["position_change"]),
                axis=1
            )
            # Adjust returns for cost
            asset_capital = total_capital / len(data_dict)
            data["returns_net"] = data["returns"] - data["transaction_cost"] / asset_capital
            data["portfoliovalue"] = (1 + data["returns_net"].fillna(0)).cumprod() * asset_capital
        else:
            asset_capital = total_capital / len(data_dict)
            data["portfoliovalue"] = (1 + data["returns"].fillna(0)).cumprod() * asset_capital

        self.history[symbol] = data

    combined = pd.concat([df["portfoliovalue"] for df in self.history.values()], axis=1)
    combined.columns = list(self.history.keys())
    combined["total_portfolio"] = combined.sum(axis=1)
    self.total_portfolio = combined

    return self.history, self.total_portfolio


