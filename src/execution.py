class Execution:
    def __init__(self, initial_cash=100000):
        self.cash = initial_cash
        self.positions = {}
        self.trades = []

    def execute_order(self, symbol, signal, price):
        size = abs(signal)
        if signal > 0:
            self.buy(symbol, size, price)
        elif signal < 0:
            self.sell(symbol, size, price)

    def buy(self, symbol, size, price):
        cost = size * price
        if self.cash >= cost:
            self.cash -= cost
            self.positions[symbol] = self.positions.get(symbol, 0) + size
            self.trades.append((symbol, "BUY", size, price))

    def sell(self, symbol, size, price):
        held = self.positions.get(symbol, 0)
        if held >= size:
            self.cash += size * price
            self.positions[symbol] -= size
            self.trades.append((symbol, "SELL", size, price))
