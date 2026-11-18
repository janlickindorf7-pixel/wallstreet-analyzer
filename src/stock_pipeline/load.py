import pandas as pd
from pathlib import Path 

from stock_pipeline.config import DATA_DIR
from stock_pipeline.logger import setup_logger

logger = setup_logger(__name__)

def save_stock_data(clean_df_new: pd.DataFrame, filename: str = "top10_stocks_data.csv") -> Path:

    DATA_DIR.mkdir(parents=True, exist_ok=True)
    file_path = DATA_DIR / filename 

    logger.info(f"Zapisuje {len(clean_df_new)} do pliku CSV")

    clean_df_new.to_csv(file_path)

    logger.info("Zapis zakonczony")
    return file_path