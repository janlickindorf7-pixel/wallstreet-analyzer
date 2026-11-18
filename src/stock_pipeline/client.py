import pandas as pd 
import yfinance as yf 


from stock_pipeline.logger import setup_logger 

logger = setup_logger(__name__)

SP500_URL = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
HEADERS = {"User-Agent": "Mozilla/5.0"}

def fetch_sp500_tickers() -> list[str]:
    tabela = pd.read_html(SP500_URL, storage_options=HEADERS) 
    df_sp500 = tabela[0]
    tickers = df_sp500['Symbol'].str.replace('.', '-', regex=False).tolist()

    logger.info(f"Pobrano {len(tickers)} symboli")
    return tickers 


def fetch_market_caps(tickers: list[str]) -> pd.DataFrame:
    logger.info(f"Pobieram kapitalizacje dla {len(tickers)} spolek")
    rows = []

    
    for ticker in tickers:
        try: 
            market_cap = yf.Ticker(ticker).info.get('marketCap')
        except Exception as e: 
            logger.warning(f"Nie udalo sie pobrac {ticker}: {e}")
            market_cap = None

        rows.append({"ticker": ticker, "market_cap": market_cap})

    df = pd.DataFrame(rows)
    logger.info("Pobrano kapitalizacje dla spolek!")
    return df 


def fetch_prices(tickers: list[str], period: str = "2y") -> pd.DataFrame: 
    logger.info(f"Pobieram notowania {len(tickers)} spolek, okres: {period}")

    df = yf.download(tickers, period=period, auto_adjust=False, progress=False)

    if df.empty: 
        logger.error("yfinance zwrocil pusty wynik")
        raise ValueError(f"Nie pobrano notowan dla: {tickers}")

    logger.info(f"Pobrano notowania, wymiar ramki: {df.shape}")
    return df     