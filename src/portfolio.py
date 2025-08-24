class Portfolio:
    def __init__(self, data, initial_capital=10000):
        self.data = data
        self.initial_capital = initial_capital
        self.positions = None
        self.cash = None
        self.portfolio_value = None

    def backtest(self):
        self.data["Position"] = self.data["Signal"].shift(1)
        self.data["Returns"] = self.data["Close"].pct_change() * self.data["Position"]
        self.data["PortfolioValue"] = self.initial_capital * (1 + self.data["Returns"].fillna(0)).cumprod()
        return self.data
