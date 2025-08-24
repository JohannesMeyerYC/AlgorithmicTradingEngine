import numpy as np
import pandas as pd
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

class RSI_MomentumStrategy(BaseStrategy):
    def __init__(self, symbol="AAPL", start="2022-01-01", end="2023-01-01", period=14):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.period = period
        self.data = None

    def generate_signals(self):
        dm = DataManager(self.symbol, self.start, self.end)
        dm.download_data()
        self.data = dm.data.copy()
        delta = self.data["close"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(self.period).mean()
        avg_loss = pd.Series(loss).rolling(self.period).mean()
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        self.data["signal"] = np.where(rsi < 30, 1, np.where(rsi > 70, -1, 0))
        return self.data

class MeanReversionStrategy(BaseStrategy):
    def __init__(self, symbol="AAPL", start="2022-01-01", end="2023-01-01", window=20):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.window = window
        self.data = None

    def generate_signals(self):
        dm = DataManager(self.symbol, self.start, self.end)
        dm.download_data()
        dm.add_moving_averages(short_window=self.window, long_window=self.window*2)
        self.data = dm.data.copy()
        self.data["signal"] = 0
        self.data["zscore"] = (self.data["close"] - self.data["sma20"]) / self.data["close"].rolling(self.window).std()
        self.data["signal"] = np.where(self.data["zscore"] > 1, -1, np.where(self.data["zscore"] < -1, 1, 0))
        return self.data
