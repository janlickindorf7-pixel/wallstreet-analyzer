import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from stock_pipeline.load import load_indicators

MIESIACE = {"3M": 3, "6M": 6, "1Y": 12}
NAZWY_LINII = {"close": "Close", "sma_20": "SMA 20", "sma_50": "SMA 50"}


def styl(fig):
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#1E2530",
        plot_bgcolor="#1E2530",
        font=dict(color="#FAFAFA"),
        hovermode="x unified",
    )
    return fig


@st.cache_data
def wczytaj_dane():
    return load_indicators()


st.title("🔍 Stock Details")
st.subheader("Detailed Analysis of a Selected Stock")

# --- dane ---
try:
    dane = wczytaj_dane()
except FileNotFoundError:
    st.error("Brak pliku indicators.csv. Uruchom najpierw: scripts/run_pipeline.py")
    st.stop()

# --- wybór spółki i okresu ---
ticker = st.sidebar.selectbox("Choose a stock:", sorted(dane["ticker"].unique()))
st.write(f"Selected company: **{ticker}**")

period = st.sidebar.selectbox("Choose a period:", list(MIESIACE))

data_start = dane["date"].max() - pd.DateOffset(months=MIESIACE[period])
spolka = dane[dane["ticker"] == ticker].sort_values("date")
spolka_okres = spolka[spolka["date"] >= data_start]

if spolka_okres.empty:
    st.warning("Brak danych dla wybranej spółki i okresu.")
    st.stop()

# --- KPI ---
ostatnia_cena = spolka_okres["close"].iloc[-1]
total_return_period = (
    spolka_okres["close"].iloc[-1] / spolka_okres["close"].iloc[0] - 1
) * 100
volatility_period = spolka_okres["daily_returns"].std() * 100
average_volume_period = spolka_okres["volume"].mean()

st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(label="💵 Last Closing Price", value=f"${ostatnia_cena:.2f}")
col2.metric(
    label="📈 Price Return",
    value=f"{total_return_period:.2f}%",
    delta=f"{total_return_period:.2f}%",
)
col3.metric(label="⚡ Daily Volatility", value=f"{volatility_period:.2f}%")
col4.metric(label="📊 Average Volume", value=f"{average_volume_period:,.0f}")

# --- cena + SMA ---
fig = px.line(
    spolka_okres,
    x="date",
    y=["close", "sma_20", "sma_50"],
    title=f"{ticker} Closing Prices Over Time",
    labels={"date": "Date", "value": "Price (USD)", "variable": ""},
)
fig.for_each_trace(lambda t: t.update(name=NAZWY_LINII.get(t.name, t.name)))
fig.update_layout(
    legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
)
st.plotly_chart(styl(fig), use_container_width=True)

# --- zwroty dzienne ---
zwroty = spolka_okres.assign(daily_return_pct=spolka_okres["daily_returns"] * 100)

fig = px.bar(
    zwroty,
    x="date",
    y="daily_return_pct",
    color=zwroty["daily_return_pct"] >= 0,
    color_discrete_map={True: "#00C896", False: "#FF4B4B"},
    title=f"{ticker} Daily Returns Over Time",
    labels={"date": "Date", "daily_return_pct": "Daily Return (%)"},
)
fig.update_layout(showlegend=False)
fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
st.plotly_chart(styl(fig), use_container_width=True)

# --- RSI ---
fig = px.line(
    spolka_okres,
    x="date",
    y="rsi_14",
    title=f"{ticker} RSI (14)",
    labels={"date": "Date", "rsi_14": "RSI"},
)
fig.add_hline(
    y=70, line_dash="dash", line_color="#FF4B4B", annotation_text="Overbought (70)"
)
fig.add_hline(
    y=30, line_dash="dash", line_color="#00C896", annotation_text="Oversold (30)"
)
st.plotly_chart(styl(fig), use_container_width=True)

# --- MACD ---
fig = go.Figure()
fig.add_trace(
    go.Bar(x=spolka_okres["date"], y=spolka_okres["histogram"], name="Histogram")
)
fig.add_trace(
    go.Scatter(x=spolka_okres["date"], y=spolka_okres["macd"], mode="lines", name="MACD")
)
fig.add_trace(
    go.Scatter(
        x=spolka_okres["date"], y=spolka_okres["signal"], mode="lines", name="Signal"
    )
)
fig.update_layout(
    title=f"{ticker} MACD (12, 26, 9)",
    xaxis_title="Date",
    yaxis_title="MACD Value",
)
fig.add_hline(y=0, line_dash="dash", line_color="white", opacity=0.5)
st.plotly_chart(styl(fig), use_container_width=True)