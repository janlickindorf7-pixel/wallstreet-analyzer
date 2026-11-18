# Stock Pipeline

A small data pipeline that downloads the S&P 500 company list, picks the 10 companies with the largest market capitalization, fetches their historical prices from Yahoo Finance and saves them to CSV.

The project is split into a reusable Python package (`extract → transform → load`) and thin scripts that run it.

## How it works

```
Wikipedia (S&P 500 list)
        ↓  fetch_sp500_tickers()
   ~500 tickers
        ↓  fetch_market_caps()
   ticker | market_cap
        ↓  select_top_n()          (pure logic, no network)
   top 10 companies
        ↓  fetch_prices()
   price history (Open, High, Low, Close, Volume)
        ↓  save_stock_data()
   dane/top10_stocks_data.csv
```

## Project structure

```
.
├── pyproject.toml
├── README.md
├── scripts/
│   └── run_pipeline.py        # entry point: runs the whole pipeline
├── src/
│   └── stock_pipeline/
│       ├── client.py          # extract: Wikipedia + Yahoo Finance
│       ├── transform.py       # transform: select top N by market cap
│       ├── load.py            # load: save / read CSV
│       ├── config.py          # paths and settings (.env support)
│       └── logger.py          # logging setup (console + app.log)
├── tests/
│   └── test_transform.py
└── dane/                      # generated data (not tracked by Git)
```

## Requirements

- Python 3.11+
- Internet connection (Wikipedia and Yahoo Finance)

## Installation

```bash
git clone <your-repo-url>
cd Stock_market_analyzer
pip install -e ".[dev]"
```

This installs the package in editable mode together with the development tools (pytest, ruff).

## Configuration (optional)

Create a `.env` file in the project root:

```
DEFAULT_TICKER=AAPL
```

The `.env` file is not tracked by Git.

## Usage

Run the full pipeline:

```bash
python scripts/run_pipeline.py
```

The result is saved to `dane/top10_stocks_data.csv`. Fetching market caps for all ~500 companies takes a few minutes, and Yahoo Finance may rate-limit requests.

Read the saved data back in Python:

```python
from stock_pipeline.load import load_stock_data

df = load_stock_data()
print(df.head())
```

## Tests and code quality

```bash
pytest
ruff check .
```

## Roadmap

- [ ] Retry with backoff and timeouts for API calls
- [ ] Validation of partially missing tickers in downloaded prices
- [ ] Technical indicators (SMA, RSI, MACD) as part of the package, with tests
- [ ] Streamlit dashboard reading the pipeline output
- [ ] Docker image for the pipeline
- [ ] Scheduling and orchestration (Airflow / Dagster)
- [ ] Loading data into a database / warehouse and modeling it with dbt

## Data source

Company list: Wikipedia. Prices and market capitalization: Yahoo Finance via the `yfinance` library. The data is for educational purposes only and is not financial advice.

