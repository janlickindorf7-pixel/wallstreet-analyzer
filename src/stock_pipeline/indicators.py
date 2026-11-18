import pandas as pd


def compute_sma(prices: pd.Series, window: int = 20) -> pd.Series:
    """Prosta średnia krocząca. Pierwsze window-1 wartości to NaN."""
    if window < 1:
        raise ValueError("window musi być >= 1")
    return prices.rolling(window=window).mean()

def daily_returns(prices: pd.Series) -> pd.Series:
    """Dzienny zwrot jako ułamek (0.01 = 1%). Pierwsza wartość to NaN."""
    return prices.pct_change()

def compute_rsi(prices: pd.Series, window: int = 14) -> pd.Series: 
    delta = prices.diff()
    gains = delta.clip(lower=0)      
    losses = -delta.clip(upper=0)
    avg_gain = gains.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = losses.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi