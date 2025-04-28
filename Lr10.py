class Backtester:
    def __init__(self, strategy: Strategy):
        self.strategy = strategy
        self.signals = []
        self.profit = 0.0

    def run_backtest(self, n_iterations: int = 100):
        for _ in range(n_iterations):
            df = self.strategy.generate_fake_data()
            signal = self.strategy.create_signal(df)
            if signal:
                self.signals.append(signal)
                result = self.simulate_trade(signal)
                signal.result = result
                self.profit += result

    def simulate_trade(self, signal: Signal) -> float:
        if signal.side == "BUY":
            final_price = signal.entry * np.random.uniform(0.95, 1.05)
        else:  # SELL
            final_price = signal.entry * np.random.uniform(0.95, 1.05)
        
        if (signal.side == "BUY" and final_price >= signal.take_profit) or \
           (signal.side == "SELL" and final_price <= signal.take_profit):
            return abs(signal.take_profit - signal.entry)
        elif (signal.side == "BUY" and final_price <= signal.stop_loss) or \
             (signal.side == "SELL" and final_price >= signal.stop_loss):
            return -abs(signal.entry - signal.stop_loss)
        else:
            return 0.0

    def summary(self):
        print(f"Total signals: {len(self.signals)}")
        print(f"Total profit: {round(self.profit, 2)}")
