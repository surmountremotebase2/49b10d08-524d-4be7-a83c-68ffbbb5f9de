from surmount.base_class import Strategy, TargetAllocation
from surmount.technical_indicators import EMA
from surmount.logging import log

class TradingStrategy(Strategy):

    @property
    def assets(self):
        return ["AAPL"]
        
    @property
    def interval(self):
        return "1day"

    def run(self, data):
        # Calculate the 7-period and 21-period Exponential Moving Averages (EMAs)
        ema_short = EMA("AAPL", data["ohlcv"], 7)
        ema_long = EMA("AAPL", data["ohlcv"], 21)
        
        # Initialize allocation
        allocation = 0.0
        
        if len(ema_short) > 0 and len(ema_long) > 0:
            # Check if the 7-period EMA crosses above the 21-period EMA from below
            if ema_short[-2] < ema_long[-2] and ema_short[-1] > ema_long[-1]:
                log("7-period EMA crossed above the 21-period EMA. Buying signal.")
                allocation = 1.0  # Buy (go long)
            # Check if the 7-period EMA crosses below the 21-period EMA from above
            elif ema_short[-2] > ema_long[-2] and ema_short[-1] < ema_long[-1]:
                log("7-period EMA crossed below the 21-period EMA. Selling signal.")
                allocation = 0.0  # Sell (go short)
            else:
                log("No crossover action. Holding position.")
                # Hold current position (no change in allocation)
        else:
            log("Not enough data for EMAs. No action taken.")
        
        return TargetAllocation({"AAPL": allocation})