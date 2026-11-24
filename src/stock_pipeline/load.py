from pathlib import Path
import pandas as pd

from stock_pipeline.config import DATA_DIR
from stock_pipeline.logger import setup_logger

logger = setup_logger(__name__)


def save_indicators(df: pd.DataFrame, filename: str = "indicators.csv") -> Path:
    output_dir = Path(DATA_DIR)
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / filename 

    df.to_csv(output_path, index=False)
    logger.info(f"Zapisano {len(df)} wierszy do {output_path}")
    return output_path 

def load_indicators(filename: str = "indicators.csv") -> pd.DataFrame:
    path = Path(DATA_DIR) / filename
    if not path.exists():
        raise FileNotFoundError(f"Brak pliku: {Path}") 

    df = pd.read_csv(path, parse_dates=["date"])
    logger.info(f"Wczytano {len(df)} wierszy z {path}")
    return df 

