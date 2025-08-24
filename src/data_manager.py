import yfinance as yf
import pandas as pd

class DataManager:
    def __init__(self, symbol, start, end):
        self.symbol = symbol
        self.start = start
        self.end = end
        self.data = None

    def download_data(self):
        self.data = yf.download(self.symbol, start=self.start, end=self.end, auto_adjust=True)
        return self.data


    def add_moving_averages(self, short_window=20, long_window=50):
        self.data["SMA20"] = self.data["Close"].rolling(short_window).mean()
        self.data["SMA50"] = self.data["Close"].rolling(long_window).mean()
        return self.data
