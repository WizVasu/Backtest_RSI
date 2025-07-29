# RSI Trading Strategy Backtester for Bank Nifty

This repository contains a Python script for backtesting a Relative Strength Index (RSI) based trading strategy on Bank Nifty futures data. The script uses the `backtesting.py` library to simulate the strategy's performance and includes robust risk management features like dynamic position sizing, stop-loss, and take-profit levels.

## About The Project

This tool was designed to provide a framework for systematically testing a common mean-reversion strategy on intraday financial data. It loads 1-minute data, resamples it to a 5-minute timeframe, and then runs a backtest to evaluate the profitability of buying on RSI oversold signals and selling on overbought signals.

The key focus is on **risk management**, allowing users to define risk parameters and see how they impact the strategy's performance.

## Features

  - **RSI-Based Strategy**: Implements a classic mean-reversion strategy based on the 14-period RSI.
  - **Adjustable Risk Parameters**: Easily customize key settings:
      - Stop-Loss percentage
      - Take-Profit percentage
      - Capital at risk per trade
  - **Dynamic Position Sizing**: Automatically calculates the trade size based on the stop-loss distance and the specified risk percentage of total equity.
  - **Performance Analytics**: Generates a detailed performance summary, including metrics like Sharpe Ratio, Win Rate, and Max Drawdown.
  - **Visualizations**: Automatically plots the equity curve, drawdown, and trade entries/exits on a price chart.

## Getting Started

To run this backtest on your local machine, follow these steps.

### Prerequisites

You will need Python 3 and the following libraries installed:

  - `pandas`
  - `backtesting.py`
  - `TA-Lib`

### Installation

1.  Clone this repository or download the `new.py` script.

2.  Install the necessary Python libraries:

    ```bash
    pip install pandas backtesting ta-lib
    ```

    *(Note: Installing TA-Lib can sometimes be complex. Please refer to the official [TA-Lib installation guide](https://www.google.com/search?q=https://mrjbq7.github.io/ta-lib/install.html) for your operating system.)*

3.  **Data File**: This script requires a CSV data file named `adjusted_banknifty_dataff.csv`. You must place this file in the correct directory as specified in the script or update the path in the script to point to your file's location.

    The CSV file must contain the following columns: `Date`, `Time`, `Open`, `High`, `Low`, `Close`, `Volume`, `Open Interest`.

### Usage

1.  Ensure your data file is in the correct path.
2.  Modify the strategy parameters within the script if desired. You can adjust the default `stop_loss_pct`, `take_profit_pct`, and `risk_pct` directly in the `RSIindicator` class or pass them as arguments in the `bt.run()` function.
3.  Execute the Python script:
    ```bash
    python new.py
    ```
4.  The script will print the backtest performance statistics to the console and open a browser window with the results plot.

## Strategy Explained

The trading logic is as follows:

  - **Entry Condition**: A long position is initiated when the **RSI value crosses above the `lower_bound`** (default: 30), signaling a potential end to an oversold period.
  - **Exit Condition**: The position is closed when the **RSI value crosses above the `upper_bound`** (default: 70), signaling an overbought condition.
  - **Risk Management**:
      - For every trade, the position size is calculated to risk a fixed percentage of the account equity (e.g., 1% or 2%).
      - Each trade is placed with a predefined stop-loss and take-profit order.

-----

### **Disclaimer**

This project is for educational and informational purposes only. It is not financial advice. The results from this backtest are based on historical data and do not guarantee future performance. Trading in financial markets involves substantial risk.
