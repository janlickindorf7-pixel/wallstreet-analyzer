import pandas as pd 
import pytest 
from stock_pipeline.transform import select_top_n

def test_select_top_n_zwraca_najwieksze_w_kolejnosci():
    df = pd.DataFrame({
        "ticker": ["A", "B", "C", "D", "E"],
        "market_cap": [100, None, 300, 200, 50]
    })

    wynik = select_top_n(df, n=3)

    assert wynik["ticker"].tolist() == ["C", "D", "A"]

def test_brak_kolumny_rzuca_blad():
    df = pd.DataFrame({"ticker": ["A"]})

    with pytest.raises(ValueError):
        select_top_n(df)