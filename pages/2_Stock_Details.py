import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🔍 Stock Details")
st.subheader("Detailed Analysis of a Selected Stock")

dane = pd.read_csv(
    "top10_stocks_data.csv",
    header=[0, 1],
    index_col=0,
    parse_dates=True
)

dates_sorted = dane.index.is_monotonic_increasing

st.write(f"Dates sorted ascending: {dates_sorted}")


ticker = st.sidebar.selectbox(
    "Choose a stock:",
    dane["Close"].columns
)

st.write(f"Selected company: **{ticker}**")

period = st.sidebar.selectbox(
    "Choose a period:",
    ["3M", "6M", "1Y"]
)

if period == "3M":
    data_start = dane.index.max() - pd.DateOffset(months=3)
elif period == "6M":
    data_start = dane.index.max() - pd.DateOffset(months=6)
else:
    data_start = dane.index.max() - pd.DateOffset(years=1)


full_prices = dane["Close"][ticker]
ceny = dane["Close"][ticker].loc[data_start:]
wolumen = dane["Volume"][ticker].loc[data_start:]

ostatnia_cena = ceny.iloc[-1]

total_return_period = (
    (ceny.iloc[-1] / ceny.iloc[0]) - 1
) * 100

volatility_period = ceny.pct_change().std() * 100

average_volume_period = wolumen.mean() 

delta = full_prices.diff()

gains = delta.clip(lower=0)
losses = -delta.clip(upper=0)

average_gain = gains.rolling(window=14).mean()
average_loss = losses.rolling(window=14).mean()

rs = average_gain / average_loss

rsi = 100 - (100 / (1 + rs))

rsi = rsi.loc[data_start:]


st.markdown("### 📊 Key Performance Indicators")

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    label="💵 Last Closing Price",
    value=f"${ostatnia_cena:.2f}"
)

col2.metric(
    label="📈 Price Return",
    value=f"{total_return_period:.2f}%",
    delta=f"{total_return_period:.2f}%"
)

col3.metric(
    label="⚡ Daily Volatility",
    value=f"{volatility_period:.2f}%"
)

col4.metric(
    label="📊 Average Volume",
    value=f"{average_volume_period:,.0f}"
)


sma_20 = pd.read_csv(
    "dane/sma_20.csv",
    index_col=0,
    parse_dates=True
)

sma_50 = pd.read_csv(
    "dane/sma_50.csv",
    index_col=0,
    parse_dates=True
)

sma20_filtered = sma_20[ticker].loc[data_start:]
sma50_filtered = sma_50[ticker].loc[data_start:]

fig = px.line(
    ceny,
    x=ceny.index,
    y=ceny.values,
    title=f"{ticker} Closing Prices Over Time",
    labels={
        "x": "Date",
        "y": "Closing Price (USD)"
    }
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E2530",
    plot_bgcolor="#1E2530",
    font=dict(color="#FAFAFA"),
    hovermode="x unified",
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    )
)


fig.add_scatter(
    x=sma20_filtered.index,
    y=sma20_filtered.values,
    mode="lines",
    name="SMA 20"
)

fig.add_scatter(
    x=sma50_filtered.index,
    y=sma50_filtered.values,
    mode="lines",
    name="SMA 50"
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E2530",
    plot_bgcolor="#1E2530",
    font=dict(color="#FAFAFA"),
    hovermode="x unified"
)




st.plotly_chart(fig, use_container_width=True)

daily_returns = ceny.pct_change() * 100

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E2530",
    plot_bgcolor="#1E2530",
    font=dict(color="#FAFAFA"),
    hovermode="x unified"
)

fig.add_hline(
    y=0,
    line_dash="dash",
    line_color="white",
    opacity=0.5
)

fig = px.bar(
    x=daily_returns.index,
    y=daily_returns.values,
    title=f"{ticker} Daily Returns Over Time",
    labels={
        "x": "Date",
        "y": "Daily Return (%)"
    },
    color=daily_returns >= 0,
    color_discrete_map={
        True: "#00C896",
        False: "#FF4B4B"
    }
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E2530",
    plot_bgcolor="#1E2530",
    font=dict(color="#FAFAFA"),
    hovermode="x unified"
)

fig.add_hline(
    y=0,
    line_dash="dash",
    line_color="white",
    opacity=0.5
)

st.plotly_chart(fig, use_container_width=True)

fig = px.line(
    rsi,
    x=rsi.index,
    y=rsi.values,
    title=f"{ticker} RSI (14)",
    labels={
        "x": "Date",
        "y": "RSI"
    }
)

fig.update_layout(
    template="plotly_dark",
    paper_bgcolor="#1E2530",
    plot_bgcolor="#1E2530",
    font=dict(color="#FAFAFA"),
    hovermode="x unified"
)

fig.add_hline(
    y=70,
    line_dash="dash",
    line_color="#FF4B4B",
    annotation_text="Overbought (70)"
)

fig.add_hline(
    y=30,
    line_dash="dash",
    line_color="#00C896",
    annotation_text="Oversold (30)"
)

st.plotly_chart(fig, use_container_width=True)

ema_12 = full_prices.ewm(span=12, adjust=False).mean()
ema_26 = full_prices.ewm(span=26, adjust=False).mean()

MACD_line = ema_12 - ema_26

signal_line = MACD_line.ewm(span=9, adjust=False).mean()

histogram = MACD_line - signal_line

MACD_line = MACD_line.loc[data_start:]
signal_line = signal_line.loc[data_start:]
histogram = histogram.loc[data_start:]

fig = go.Figure()

# Histogram
fig.add_trace(
    go.Bar(
        x=histogram.index,
        y=histogram.values,
        name="Histogram"
    )
)

# MACD Line
fig.add_trace(
    go.Scatter(
        x=MACD_line.index,
        y=MACD_line.values,
        mode="lines",
        name="MACD"
    )
)

fig.add_trace(
    go.Scatter(
        x=signal_line.index,
        y=signal_line.values,
        mode="lines",
        name="Signal"
    )
)

fig.update_layout(
    title=f"{ticker} MACD (12, 26, 9)",
    template="plotly_dark",
    paper_bgcolor="#1E2530",
    plot_bgcolor="#1E2530",
    font=dict(color="#FAFAFA"),
    hovermode="x unified",
    xaxis_title="Date",
    yaxis_title="MACD Value"
)

fig.add_hline(
    y=0,
    line_dash="dash",
    line_color="white",
    opacity=0.5
)

st.plotly_chart(fig, use_container_width=True)