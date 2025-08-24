class Execution:
    def __init__(self):
        self.trades = []

    def execute_trade(self, signal, price):
        if signal == 1:
            self.trades.append(("BUY", price))
        elif signal == -1:
            self.trades.append(("SELL", price))
