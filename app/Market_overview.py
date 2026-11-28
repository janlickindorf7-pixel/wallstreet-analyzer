import streamlit as st
import pandas as pd
import plotly.express as px
from stock_pipeline.load import load_indicators 

st.title("📊 Market Overview")
st.subheader("Comparison of Top 10 Stocks")

@st.cache_data
def wczytaj_wskazniki():
    return load_indicators()

dane = wczytaj_wskazniki()

period = st.sidebar.selectbox("Choose a period:", ["3M", "6M", "1Y"])

if period == "3M":
    data_start = dane["date"].max() - pd.DateOffset(months=3)
elif period == "6M":
    data_start = dane["date"].max() - pd.DateOffset(months=6)
else:
    data_start = dane["date"].max() - pd.DateOffset(years=1)

dane_okres = dane[dane["date"] >= data_start].sort_values(["ticker", "date"]).copy()


dane_okres["normalized"] = (
    100 * dane_okres["close"] / dane_okres.groupby("ticker")["close"].transform("first")
)

fig = px.line(
    dane_okres,
    x="date",
    y="normalized",
    color="ticker",
    title="Normalized Performance of Top 10 Stocks",
    labels={"date": "Date", "normalized": "Normalized Price (Base = 100)"},
)
st.plotly_chart(fig, use_container_width=True)

dane_okres["daily_returns_pct"] = dane_okres["daily_returns"] * 100

volatility_all = (
    dane_okres.groupby("ticker")["daily_returns"].std() * 100
).sort_values(ascending=False)

fig = px.bar(
    x=volatility_all.index,
    y=volatility_all.values,
    title="Volatility of Top 10 Stocks",
    labels={
        "x": "Stock",
        "y": "Volatility (%)"
    }
)

st.plotly_chart(fig, use_container_width=True)

average_volume_all = (
    dane_okres.groupby("ticker")["volume"].mean().sort_values(ascending=False)
)

fig = px.bar(
    x=average_volume_all.index,
    y=average_volume_all.values,
    title="Average Trading Volume of Top 10 Stocks",
    labels={
        "x": "Stock",
        "y": "Average Daily Volume"
    }
)

st.plotly_chart(fig, use_container_width=True)