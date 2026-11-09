import streamlit as st

st.set_page_config(
    page_title="WallStreet Analyzer",
    page_icon="📈",
    layout="wide"
)

st.title("📈 WallStreet Analyzer")

st.subheader("Stock Market Analytics Dashboard")

st.write(
    "Welcome to WallStreet Analyzer! "
    "Explore market performance and analyze individual stocks."
)

st.info(
    "Use the navigation menu on the left to explore "
    "Market Overview and Stock Details."
)