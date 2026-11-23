from stock_pipeline.client import fetch_market_caps, fetch_prices, fetch_sp500_tickers
from stock_pipeline.load import save_stock_data
from stock_pipeline.transform import select_top_n


def main() -> None:
    tickers = fetch_sp500_tickers()
    caps = fetch_market_caps(tickers)
    top = select_top_n(caps, n=10)
    prices = fetch_prices(top["ticker"].tolist())
    save_stock_data(prices)


if __name__ == "__main__":
    main()
