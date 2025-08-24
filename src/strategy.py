import numpy as np
from data_manager import DataManager

class MovingAverageStrategy:
    def __init__(self, symbol="AAPL", start="2022-01-01", end="2023-01-01"):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = None

    def generate_signals(self):
        dm = DataManager(self.symbol, self.start, self.end)
        self.data = dm.download_data().copy()
        self.data = dm.add_moving_averages(short_window=20, long_window=50)
        self.data["Signal"] = 0
        self.data.iloc[20:, self.data.columns.get_loc("Signal")] = np.where(
            self.data["SMA20"].iloc[20:] > self.data["SMA50"].iloc[20:], 1, -1
        )
        return self.data
