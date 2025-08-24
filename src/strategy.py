import numpy as np
from data_manager import DataManager

class BaseStrategy:
    def generate_signals(self):
        raise NotImplementedError

class MovingAverageStrategy(BaseStrategy):
    def __init__(self, symbol="AAPL", start="2022-01-01", end="2023-01-01"):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = None

    def generate_signals(self):
        dm = DataManager(self.symbol, self.start, self.end)
        dm.download_data()
        dm.add_moving_averages()
        self.data = dm.data.copy()
        self.data["signal"] = 0
        self.data.iloc[20:, self.data.columns.get_loc("signal")] = np.where(
            self.data["sma20"].iloc[20:] > self.data["sma50"].iloc[20:], 1, -1
        )
        return self.data
