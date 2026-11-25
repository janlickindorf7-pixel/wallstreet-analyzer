import pandas as pd
import pytest

from stock_pipeline.load import (
    load_indicators,
    load_stock_data,
    save_indicators,
    save_stock_data,
)


@pytest.fixture
def indicators_df():
    return pd.DataFrame(
        {
            "date": pd.date_range("2026-01-01", periods=3),
            "ticker": ["AAA", "AAA", "AAA"],
            "close": [1.0, 2.0, 3.0],
            "sma_20": [None, None, 2.0],
        }
    )


def test_zapis_i_odczyt_to_para(tmp_path, monkeypatch, indicators_df):
    monkeypatch.setattr("stock_pipeline.load.DATA_DIR", tmp_path)

    sciezka = save_indicators(indicators_df)

    assert sciezka == tmp_path / "indicators.csv"
    assert sciezka.exists()
    pd.testing.assert_frame_equal(indicators_df, load_indicators())


def test_zapis_tworzy_brakujacy_folder(tmp_path, monkeypatch, indicators_df):
    nowy = tmp_path / "a" / "b"
    monkeypatch.setattr("stock_pipeline.load.DATA_DIR", nowy)

    sciezka = save_indicators(indicators_df)

    assert sciezka.exists()


def test_brak_pliku_rzuca_blad_z_nazwa(tmp_path, monkeypatch):
    monkeypatch.setattr("stock_pipeline.load.DATA_DIR", tmp_path)

    with pytest.raises(FileNotFoundError, match="nie_ma.csv"):
        load_indicators("nie_ma.csv")


def test_stock_data_zapis_i_odczyt_to_para(tmp_path, monkeypatch):
    monkeypatch.setattr("stock_pipeline.load.DATA_DIR", tmp_path)

    idx = pd.date_range("2026-01-01", periods=3, name="Date")
    cols = pd.MultiIndex.from_product(
        [["Close", "Volume"], ["AAA", "BBB"]], names=["Price", "Ticker"]
    )
    df = pd.DataFrame(1.0, index=idx, columns=cols)

    save_stock_data(df)

    pd.testing.assert_frame_equal(df, load_stock_data(), check_freq=False)
