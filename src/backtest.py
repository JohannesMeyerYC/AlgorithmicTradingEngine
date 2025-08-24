import matplotlib.pyplot as plt
import subprocess

class Backtest:
    def __init__(self, data):
        self.data = data

    def plot_results(self):
        plt.figure(figsize=(12, 6))
        plt.plot(self.data["close"], label="Close Price")

        for col in ["sma20", "sma50", "portfoliovalue"]:
            if col in self.data.columns:
                plt.plot(self.data[col], label=col.capitalize())

        plt.legend()
        plt.title("Backtest Results")
        tmp_file = "backtest_demo.png"
        plt.savefig(tmp_file)
        subprocess.run(["explorer.exe", tmp_file])
