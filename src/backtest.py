import matplotlib.pyplot as plt
import subprocess

class Backtest:
    def __init__(self, data_dict):
        self.data_dict = data_dict

    def plot_results(self):
        for symbol, data in self.data_dict.items():
            plt.figure(figsize=(12, 6))
            plt.plot(data["close"], label=f"{symbol} Close Price")

            for col in ["sma20", "sma50", "portfoliovalue"]:
                if col in data.columns:
                    plt.plot(data[col], label=f"{symbol} {col.capitalize()}")

            plt.legend()
            plt.title(f"Backtest Results: {symbol}")
            tmp_file = f"backtest_{symbol}.png"
            plt.savefig(tmp_file)
            subprocess.run(["explorer.exe", tmp_file])
