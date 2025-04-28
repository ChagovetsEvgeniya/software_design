import pandas as pd
import numpy as np
import ta  # pip install ta
from dataclasses import dataclass
from datetime import datetime
import matplotlib.pyplot as plt

# Data class to represent a trade
@dataclass
class Trade:
    entry_time: datetime
    entry_price: float
    exit_time: datetime
    exit_price: float
    side: str  # "LONG" or "SHORT"
    profit_pct: float  # Profit percentage

# Trading strategy class
class Strategy:
    def __init__(self, tp_pct=0.02, sl_pct=0.01):
        self.tp_pct = tp_pct  # Take profit percentage
        self.sl_pct = sl_pct  # Stop loss percentage
        self.trades = []      # List to store trades

    # Generate technical indicators and add them to the DataFrame
    def generate_indicators(self, df):
        df['ema_12'] = ta.trend.ema_indicator(df['close'], window=12)
        df['ema_26'] = ta.trend.ema_indicator(df['close'], window=26)
        df['rsi'] = ta.momentum.rsi(df['close'], window=14)
        df['cci'] = ta.trend.cci(df['high'], df['low'], df['close'], window=14)
        df['macd'] = ta.trend.macd(df['close'], window_slow=36, window_fast=14)
        df['macd_signal'] = ta.trend.macd_signal(df['close'], window_slow=36, window_fast=14)
        return df

    # Condition to enter a LONG position
    def check_entry_long(self, row):
        return (row['cci'] < -200) and (row['macd'] > row['macd_signal'])

    # Condition to enter a SHORT position
    def check_entry_short(self, row):
        return (row['rsi'] > 70) and (row['ema_26'] > row['ema_12'])

    # Main backtesting loop
    def backtest(self, df):
        position = None     # Current position: None, "LONG", "SHORT"
        entry_price = 0      # Price at which position was opened
        for i in range(len(df)):
            row = df.iloc[i]
            if position is None:
                if self.check_entry_long(row):
                    position = "LONG"
                    entry_price = row['close']
                    entry_time = row['time']
                elif self.check_entry_short(row):
                    position = "SHORT"
                    entry_price = row['close']
                    entry_time = row['time']
            else:
                if position == "LONG":
                    # Check if take profit or stop loss is reached
                    if row['close'] >= entry_price * (1 + self.tp_pct):
                        self.trades.append(Trade(entry_time, entry_price, row['time'], row['close'], "LONG", (row['close'] - entry_price) / entry_price * 100))
                        position = None
                    elif row['close'] <= entry_price * (1 - self.sl_pct):
                        self.trades.append(Trade(entry_time, entry_price, row['time'], row['close'], "LONG", (row['close'] - entry_price) / entry_price * 100))
                        position = None
                elif position == "SHORT":
                    if row['close'] <= entry_price * (1 - self.tp_pct):
                        self.trades.append(Trade(entry_time, entry_price, row['time'], row['close'], "SHORT", (entry_price - row['close']) / entry_price * 100))
                        position = None
                    elif row['close'] >= entry_price * (1 + self.sl_pct):
                        self.trades.append(Trade(entry_time, entry_price, row['time'], row['close'], "SHORT", (entry_price - row['close']) / entry_price * 100))
                        position = None

    # Calculate and return performance metrics
    def performance(self):
        profits = [trade.profit_pct for trade in self.trades]
        win_trades = [p for p in profits if p > 0]
        loss_trades = [p for p in profits if p <= 0]
        pf = sum(win_trades) / abs(sum(loss_trades)) if sum(loss_trades) != 0 else float('inf')  # Profit Factor
        wr = len(win_trades) / len(profits) * 100 if profits else 0  # Win Rate
        pnl = sum(profits)  # Total profit/loss percentage
        max_drawdown = self.calculate_max_drawdown(profits)  # Maximum drawdown percentage
        return {"Profit Factor": pf, "Win Rate": wr, "PnL%": pnl, "Max Drawdown%": max_drawdown}

    # Calculate maximum drawdown
    def calculate_max_drawdown(self, profits):
        cumulative = np.cumsum(profits)
        peak = np.maximum.accumulate(cumulative)
        drawdown = (peak - cumulative) / peak
        return np.max(drawdown) * 100

# Function to generate synthetic (random) historical data
def load_data():
    dates = pd.date_range(start="2023-01-01", periods=100000, freq="T")  # Every minute
    prices = np.cumsum(np.random.randn(len(dates)) * 0.5) + 1000  # Random walk around 1000
    return pd.DataFrame({
        'time': dates,
        'open': prices,
        'high': prices + np.random.rand(len(dates)),
        'low': prices - np.random.rand(len(dates)),
        'close': prices,
        'volume': np.random.rand(len(dates))
    })

# Entry point
if __name__ == "__main__":
    df = load_data()
    strategy = Strategy(tp_pct=0.03, sl_pct=0.015)  # Initialize strategy with custom TP and SL
    df = strategy.generate_indicators(df)  # Calculate indicators
    strategy.backtest(df)  # Run backtest
    stats = strategy.performance()  # Get performance results
    print(stats)
    
    # Plotting the results
    plt.figure(figsize=(12,6))
    
    # Plot the closing price
    plt.plot(df['time'], df['close'], label='Close Price', color='blue')
    
    # Plot buy/sell signals
    for trade in strategy.trades:
        if trade.side == 'LONG':
            plt.scatter(trade.entry_time, trade.entry_price, marker='^', color='green', label='Buy Signal' if trade == strategy.trades[0] else "")
            plt.scatter(trade.exit_time, trade.exit_price, marker='v', color='red', label='Sell Signal' if trade == strategy.trades[0] else "")
        elif trade.side == 'SHORT':
            plt.scatter(trade.entry_time, trade.entry_price, marker='v', color='red', label='Sell Signal' if trade == strategy.trades[0] else "")
            plt.scatter(trade.exit_time, trade.exit_price, marker='^', color='green', label='Buy Signal' if trade == strategy.trades[0] else "")
    
    plt.title('Price and Trade Signals')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend(loc='best')
    plt.show()
