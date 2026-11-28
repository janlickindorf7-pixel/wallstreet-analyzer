from stock_pipeline.client import fetch_market_caps, fetch_prices, fetch_sp500_tickers
from stock_pipeline.indicators import build_indicators
from stock_pipeline.load import load_stock_data, save_indicators, save_stock_data
from stock_pipeline.transform import select_top_n


def main() -> None:

    # --- etap 1: surowe dane ---
    tickers = fetch_sp500_tickers()
    caps = fetch_market_caps(tickers)
    top = select_top_n(caps, n=10)
    prices = fetch_prices(top["ticker"].tolist(), period="2y")
    save_stock_data(prices)

    # --- etap 2: wskazniki z zapisanego pliku ---
    raw = load_stock_data()
    indicators = build_indicators(raw)
    save_indicators(indicators)


if __name__ == "__main__":
    main()
