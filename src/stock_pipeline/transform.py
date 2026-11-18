import pandas as pd
from stock_pipeline.logger import setup_logger


logger = setup_logger(__name__)

def select_top_n(df: pd.DataFrame, n: int = 10) -> pd.DataFrame:
    
    logger.info("Rozpoczynam sortowanie top10 spolek pod wzgledem kapitalizacji.")

    if "market_cap" not in df.columns:
        raise ValueError("Brak kolumny 'market_cap' w danych wejściowych")


    df_sorted_new = df.sort_values(by="market_cap", ascending=False).iloc[:n]
    clean_df_new = df_sorted_new.dropna()



    logger.info(f"Wybrano {len(clean_df_new)} spółek")
    return clean_df_new