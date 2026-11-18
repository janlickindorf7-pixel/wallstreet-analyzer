import os 
from pathlib import Path 
from dotenv import load_dotenv 
from stock_pipeline.logger import setup_logger 

logger = setup_logger(__name__)

load_dotenv()

BASE_DIR:   Path = Path(__file__).resolve().parent.parent.parent
DATA_DIR:   Path = BASE_DIR / "dane"

DEFAULT_TICKER: str = os.getenv("DEFAULT_TICKER", "AAPL")

logger.info(f"Katalog główny projektu ustalony na: {BASE_DIR}")
logger.info(f"Katalog danych ustalony na: {DATA_DIR}")