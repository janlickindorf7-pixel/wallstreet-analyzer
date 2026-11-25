import pandas as pd

from stock_pipeline.logger import setup_logger

logger = setup_logger(__name__)


def compute_sma(prices: pd.Series, window: int = 20) -> pd.Series:
    """Prosta średnia krocząca. Pierwsze window-1 wartości to NaN."""
    if window < 1:
        raise ValueError("window musi być >= 1")
    return prices.rolling(window=window).mean()


def daily_returns(prices: pd.Series) -> pd.Series:
    """Dzienny zwrot jako ułamek (0.01 = 1%). Pierwsza wartość to NaN."""
    return prices.pct_change()


def compute_rsi(prices: pd.Series, window: int = 14) -> pd.Series:

    if window < 1:
        raise ValueError("window musi byc >= 1")

    delta = prices.diff()
    gains = delta.clip(lower=0)
    losses = -delta.clip(upper=0)
    avg_gain = gains.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()
    avg_loss = losses.ewm(alpha=1 / window, adjust=False, min_periods=window).mean()

    rs = avg_gain / avg_loss
    rsi = 100 - (100 / (1 + rs))

    return rsi


def compute_macd(
    prices: pd.Series, fast: int = 12, slow: int = 26, signal: int = 9
) -> pd.DataFrame:
    """MACD (domyślnie 12, 26, 9).

    Zwraca kolumny: macd, signal, histogram. Bez NaN na początku serii,
    ale przez pierwsze ~slow dni wartości są mało wiarygodne.
    """
    ema_fast = prices.ewm(span=fast, adjust=False).mean()
    ema_slow = prices.ewm(span=slow, adjust=False).mean()
    macd_line = ema_fast - ema_slow
    signal_line = macd_line.ewm(span=signal, adjust=False).mean()
    histogram = macd_line - signal_line

    return pd.DataFrame(
        {"macd": macd_line, "signal": signal_line, "histogram": histogram},
        index=prices.index,
    )


def build_indicators(prices: pd.DataFrame) -> pd.DataFrame:
    for level in ("Close", "Volume"):
        if level not in prices.columns.get_level_values(0):
            raise ValueError(f"Brak '{level} w danych wejsciowych")

    close = prices["Close"]
    volume = prices["Volume"]

    frames = []

    for ticker in close.columns:
        c = close[ticker]
        frame = pd.DataFrame(
            {
                "close": c,
                "volume": volume[ticker],
                "daily_returns": daily_returns(c),
                "sma_20": compute_sma(c, 20),
                "sma_50": compute_sma(c, 50),
                "rsi_14": compute_rsi(c),
            }
        )
        macd = compute_macd(c)

        frame = frame.join(macd)
        frame["ticker"] = ticker
        frames.append(frame)

    result = pd.concat(frames)
    result.index.name = "date"
    result = result.reset_index()

    first = ["date", "ticker"]
    result = result[first + [c for c in result.columns if c not in first]]

    logger.info(f"Policzono wskazniki dla {len(frames)} spolek, wierszy: {len(result)}")
    return result
