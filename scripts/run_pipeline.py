from stock_pipeline.client import fetch_sp500_tickers, fetch_market_caps, fetch_prices
from stock_pipeline.transform import select_top_n
from stock_pipeline.load import save_stock_data

def main() -> None:
    tickers = fetch_sp500_tickers()
    caps = fetch_market_caps(tickers)
    top = select_top_n(caps, n=10)
    prices = fetch_prices(top["ticker"].tolist())
    save_stock_data(prices)

if __name__ == "__main__":
    main()