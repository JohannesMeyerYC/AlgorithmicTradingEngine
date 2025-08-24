import matplotlib.pyplot as plt
import subprocess

class Backtest:
    def __init__(self, data):
        self.data = data

    def plot_results(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data["Close"], label="Close Price")
        plt.plot(self.data["SMA20"], label="SMA20")
        plt.plot(self.data["SMA50"], label="SMA50")
        plt.plot(self.data["PortfolioValue"], label="Portfolio Value")
        plt.legend()
        plt.title("Backtest Results")
        tmp_file = "backtest_demo.png"
        plt.savefig(tmp_file)
        subprocess.run(["explorer.exe", tmp_file])
