from pathlib import Path

import pandas as pd

from stock_pipeline.config import DATA_DIR
from stock_pipeline.logger import setup_logger

logger = setup_logger(__name__)


def save_indicators(df: pd.DataFrame, filename: str = "indicators.csv") -> Path:
    """Zapisuje tabelę wskaźników (format long) do CSV w dane/."""

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename

    df.to_csv(file_path, index=False)
    logger.info(f"Zapisano {len(df)} wierszy do {file_path}")
    return file_path


def load_indicators(filename: str = "indicators.csv") -> pd.DataFrame:
    """Wczytuje tabelę wskaźników z dane/ (kolumna date jako daty)."""
    file_path = DATA_DIR / filename
    if not file_path.exists():
        raise FileNotFoundError(f"Brak pliku: {file_path}")

    df = pd.read_csv(file_path, parse_dates=["date"])
    logger.info(f"Wczytano {len(df)} wierszy z {file_path}")
    return df
