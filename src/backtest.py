import matplotlib.pyplot as plt
import subprocess

class Backtest:
    def __init__(self, data_dict):
        """
        data_dict: dictionary where keys are symbols and values are their DataFrames
        Each DataFrame must have at least: 'close' and 'portfoliovalue'
        """
        self.data_dict = data_dict

    def plot_results(self):
        plt.figure(figsize=(14, 7))

        for symbol, df in self.data_dict.items():
            if "close" in df.columns:
                plt.plot(df["close"], label=f"{symbol} Close")
            if "portfoliovalue" in df.columns:
                plt.plot(df["portfoliovalue"], label=f"{symbol} Portfolio")

        total_pf = sum(df["portfoliovalue"] for df in self.data_dict.values())
        plt.plot(total_pf, label="Total Portfolio", linewidth=2, color="black")

        plt.title("Backtest Results (Multi-Asset)")
        plt.xlabel("Date")
        plt.ylabel("Price / Portfolio Value")
        plt.legend()
        plt.grid(True)

        tmp_file = "backtest_total.png"
        plt.savefig(tmp_file)
        subprocess.run(["explorer.exe", tmp_file])
