import pandas as pd
import pytest

from stock_pipeline.indicators import (
    compute_macd,
    compute_rsi,
    compute_sma,
    daily_returns,
)


def test_sma_3_na_prostej_serii():
    s = pd.Series([1, 2, 3, 4, 5], dtype=float)
    wynik = compute_sma(s, window=3)
    assert wynik.iloc[2] == 2.0
    assert wynik.iloc[4] == 4.0


def test_sma_pierwsze_wartosci_to_nan():
    s = pd.Series([1, 2, 3, 4, 5], dtype=float)
    wynik = compute_sma(s, window=3)
    assert wynik.iloc[:2].isna().all()


def test_sma_zla_wartosc_window():
    with pytest.raises(ValueError):
        compute_sma(pd.Series([1.0, 2.0]), window=0)


def test_daily_returns_na_prostej_serii():
    s = pd.Series([100.0, 110.0, 99.0])
    wynik = daily_returns(s)

    assert pd.isna(wynik.iloc[0])
    assert wynik.iloc[1] == pytest.approx(0.10)
    assert wynik.iloc[2] == pytest.approx(-0.10)


def test_rsi_same_wzrosty_to_100():
    s = pd.Series(range(1, 40), dtype=float)
    wynik = compute_rsi(s).dropna()
    assert (wynik == 100).all()


def test_rsi_zawsze_w_zakresie_0_100():
    s = pd.Series(
        [
            10,
            11,
            10.5,
            12,
            11,
            13,
            12.5,
            14,
            13,
            15,
            14,
            16,
            15,
            17,
            16,
            18,
            17,
            19,
            18,
            20,
        ],
        dtype=float,
    )
    wynik = compute_rsi(s).dropna()
    assert ((wynik >= 0) & (wynik <= 100)).all()


def test_rsi_pierwsze_wartosci_to_nan():
    s = pd.Series(range(1, 40), dtype=float)
    assert compute_rsi(s, window=14).iloc[:14].isna().all()


def test_macd_seria_stala_daje_zera():
    s = pd.Series([1.0] * 60)
    wynik = compute_macd(s)
    assert wynik.to_numpy() == pytest.approx(0.0)


def test_macd_ksztalt_i_kolumny():
    s = pd.Series(range(1, 61), dtype=float)
    wynik = compute_macd(s)
    assert list(wynik.columns) == ["macd", "signal", "histogram"]
    assert len(wynik) == len(s)
    assert wynik.index.equals(s.index)


def test_macd_histogram_to_macd_minus_signal():
    s = pd.Series([10, 12, 11, 13, 15, 14, 16, 18, 17, 19], dtype=float)
    wynik = compute_macd(s, fast=3, slow=5, signal=3)
    pd.testing.assert_series_equal(
        wynik["histogram"], wynik["macd"] - wynik["signal"], check_names=False
    )


def test_macd_dodatni_na_rosnacej_serii():
    s = pd.Series(range(1, 80), dtype=float)
    assert compute_macd(s)["macd"].iloc[-1] > 0


def test_macd_reczne_obliczenie():
    # fast=1 -> alpha=1 (EMA = cena), slow=3 -> alpha=0.5, signal=3 -> alpha=0.5
    # ceny: 10, 12
    # ema_slow: 10, 0.5*10 + 0.5*12 = 11   -> macd: 0, 1
    # signal:   0, 0.5*0 + 0.5*1 = 0.5      -> histogram: 0, 0.5
    s = pd.Series([10.0, 12.0])
    wynik = compute_macd(s, fast=1, slow=3, signal=3)
    assert wynik["macd"].tolist() == pytest.approx([0.0, 1.0])
    assert wynik["signal"].tolist() == pytest.approx([0.0, 0.5])
    assert wynik["histogram"].tolist() == pytest.approx([0.0, 0.5])
