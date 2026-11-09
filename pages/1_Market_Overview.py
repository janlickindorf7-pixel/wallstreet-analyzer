import streamlit as st
import pandas as pd
import plotly.express as px

st.title("📊 Market Overview")
st.subheader("Comparison of Top 10 Stocks")

dane = pd.read_csv(
    "top10_stocks_data.csv",
    header=[0, 1],
    index_col=0,
    parse_dates=True
)

period = st.sidebar.selectbox("Choose a period:", ["3M", "6M", "1Y"])

if period == "3M":
    data_start = dane.index.max() - pd.DateOffset(months=3)
elif period == "6M":
    data_start = dane.index.max() - pd.DateOffset(months=6)
else:
    data_start = dane.index.max() - pd.DateOffset(years=1)

ceny_wszystkie = dane["Close"].loc[data_start:]

st.success("Market data loaded successfully!")

normalized_performance = 100 * ceny_wszystkie / ceny_wszystkie.iloc[0]

fig = px.line(
    normalized_performance,
    title="Normalized Performance of Top 10 Stocks",
    labels={
        "index": "Date",
        "value": "Normalized Price (Base = 100)"
    }
)

st.plotly_chart(fig, use_container_width=True)

daily_returns_all = ceny_wszystkie.pct_change() * 100

volatility_all = daily_returns_all.std().sort_values(
    ascending=False
)

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

volume_all = dane["Volume"].loc[data_start:]

average_volume_all = volume_all.mean().sort_values(
    ascending=False
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