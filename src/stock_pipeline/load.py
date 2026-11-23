import pandas as pd


def compute_sma(prices: pd.Series, window: int = 20) -> pd.Series:
    """Prosta średnia krocząca. Pierwsze window-1 wartości to NaN."""
    if window < 1:
        raise ValueError("window musi być >= 1")
    return prices.rolling(window=window).mean()


def daily_returns(prices: pd.Series) -> pd.Series:
    """Dzienny zwrot jako ułamek (0.01 = 1%). Pierwsza wartość to NaN."""
    return prices.pct_change()
