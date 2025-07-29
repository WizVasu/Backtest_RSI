from backtesting import Backtest, Strategy
from backtesting.lib import crossover
import pandas as pd
import talib

# Load data
df = pd.read_csv("C:\\python prog\\Algo trading course coursera\\adjusted_banknifty_dataff.csv")
df['datetime'] = pd.to_datetime(df['Date'] + ' ' + df['Time'])
df.set_index('datetime', inplace=True)
df.drop(columns=['Unnamed: 9', 'Unnamed: 10'], inplace=True, errors='ignore')
df.sort_index(inplace=True)

# Resample to 5-min candles
df_resampled = df.resample('5T').agg({
    'Open': 'first',
    'High': 'max',
    'Low': 'min',
    'Close': 'last',
    'Volume': 'sum',
    'Open Interest': 'last',
    'ratio': 'last',
    'cumulative_ratio': 'last'
}).dropna()

# RSI Strategy with user-adjustable risk settings
class RSIindicator(Strategy):
    upper_bound = 70
    lower_bound = 30

    stop_loss_pct = 0.02      # Default 2% stop-loss
    take_profit_pct = 0.04    # Default 4% take-profit
    risk_pct = 0.01           # Default 1% of capital risked per trade
    slippage_pct = 0.001      # Optional slippage simulation (0.1%)

    def init(self):
        self.rsi = self.I(talib.RSI, self.data.Close, 14)

    def next(self):
        price = self.data.Close[-1]
        entry_price = price * (1 + self.slippage_pct)

        if self.position:
            if crossover(self.rsi, self.upper_bound):
                self.position.close()
        else:
            if crossover(self.lower_bound, self.rsi):
                # Risk control
                equity = self.equity
                risk_amount = self.risk_pct * equity

                stop_loss_price = entry_price * (1 - self.stop_loss_pct)
                take_profit_price = entry_price * (1 + self.take_profit_pct)

                sl_distance = entry_price - stop_loss_price
                if sl_distance <= 0:
                    return

                size = risk_amount // sl_distance

                self.buy(
                    size=int(size),
                    sl=stop_loss_price,
                    tp=take_profit_price
                )

# Example: custom SL/TP via strategy_kwargs
bt = Backtest(
    df_resampled,
    RSIindicator,
    cash=1_000_000,
    commission=0.001,
    exclusive_orders=True
)

# Run with 3% SL and 6% TP (user-defined)
stats = bt.run(
    stop_loss_pct=0.03,
    take_profit_pct=0.06,
    risk_pct=0.02  # Risk 2% of capital per trade
)

print(stats)
bt.plot(resample=False)
