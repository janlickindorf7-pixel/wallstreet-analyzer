import pandas as pd 
import pytest 
from stock_pipeline.indicators import compute_sma, daily_returns, compute_rsi

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
    s = pd.Series([10, 11, 10.5, 12, 11, 13, 12.5, 14, 13, 15,
                   14, 16, 15, 17, 16, 18, 17, 19, 18, 20], dtype=float)
    wynik = compute_rsi(s).dropna()
    assert ((wynik >= 0) & (wynik <= 100)).all()

def test_rsi_pierwsze_wartosci_to_nan():
    s = pd.Series(range(1, 40), dtype=float)
    assert compute_rsi(s, window=14).iloc[:14].isna().all()