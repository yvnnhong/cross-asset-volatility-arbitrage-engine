import pandas as pd
import numpy as np

def calculate_spread(vol1, vol2):
    """Calculate normalized volatility spread between two assets."""
    spread = vol1 - vol2
    z_score = (spread - spread.mean()) / spread.std()
    return z_score

def generate_signals(z_score, entry_threshold=1.5, exit_threshold=0.0):
    """Generate trading signals based on z-score thresholds."""
    signals = pd.Series(0, index=z_score.index)
    position = 0
    for i in range(1, len(z_score)):
        if position == 0:
            if z_score[i] > entry_threshold:
                signals[i] = -1  # Short asset 1, long asset 2
                position = -1
            elif z_score[i] < -entry_threshold:
                signals[i] = 1   # Long asset 1, short asset 2
                position = 1
        elif position == 1 and z_score[i] >= exit_threshold:
            signals[i] = 0
            position = 0
        elif position == -1 and z_score[i] <= -exit_threshold:
            signals[i] = 0
            position = 0
    return signals