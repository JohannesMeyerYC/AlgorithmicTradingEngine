import yfinance as yf
import pandas as pd

class DataManager:
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = None

    def download_data(self):
        self.data = yf.download(self.symbol, start=self.start, end=self.end, auto_adjust=False)
        
        if isinstance(self.data.columns, pd.MultiIndex):
            self.data.columns = self.data.columns.get_level_values(0)

        self.data.columns = [col.lower() for col in self.data.columns]

        if "close" not in self.data.columns and "adj close" in self.data.columns:
            self.data["close"] = self.data["adj close"]
        return self.data

    def add_moving_averages(self, short_window=20, long_window=50):
        self.data["sma20"] = self.data["close"].rolling(short_window).mean()
        self.data["sma50"] = self.data["close"].rolling(long_window).mean()
        return self.data