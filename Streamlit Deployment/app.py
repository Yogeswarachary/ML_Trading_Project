import streamlit as st
import pandas as pd
import io
import requests
import glob
import os

# DATA LAYER
@st.cache_data
def load_raw():
    """Load main ML trading dataset from GitHub"""
    url = "https://raw.githubusercontent.com/Yogeswarachary/ML_Trading_Project/main/CSV%20Data/ml_trading_data.csv"
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text))
    return df


@st.cache_data
def load_latest_trading_results():
    """Load latest trading results CSV from GitHub"""
    # GitHub folder containing the results
    base_url = "https://raw.githubusercontent.com/Yogeswarachary/ML_Trading_Project/main/Streamlit%20Deployment/"
    
    # Known result files (optional — if you prefer to list them manually)
    filenames = [
        "trading_results_2026-01-07.csv",
        "trading_results_2026-01-05.csv"
    ]

    # Try to load the most recent valid one
    for filename in sorted(filenames, reverse=True):
        file_url = base_url + filename
        response = requests.get(file_url)
        if response.status_code == 200:
            df = pd.read_csv(io.StringIO(response.text))
            st.info(f"Loaded: **{filename}** from GitHub")
            return df, filename

    # If none found
    st.error("❌ No trading_results CSVs found on GitHub. Please upload to `/Streamlit Deployment/` folder.")
    st.stop()

# MAIN DASHBOARD
st.set_page_config(page_title="ML Alpha Trading Dashboard", layout="wide")
st.title("ML Alpha Trading – Performance Dashboard")

# Load data
df_trades, file_used = load_latest_trading_results()
df_raw = load_raw()

# KPI CARDS
st.markdown("## Strategy Performance KPIs")

latest_metrics = df_trades.iloc[0]

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📈 Sharpe Ratio", f"{latest_metrics.get('sharpe', 0):.3f}")
with col2:
    st.metric("🏆 Win Rate", f"{latest_metrics.get('win_rate', 0):.1%}")
with col3:
    st.metric("📉 Max Drawdown", f"{latest_metrics.get('max_dd', 0):.1%}")
with col4:
    st.metric("🔄 Turnover", f"{latest_metrics.get('turnover', 0):.1f}")

# RAW TRADING RESULTS
st.markdown("## Raw Trading Results")
st.dataframe(df_trades.head(5), use_container_width=True)

# RAW DATA PREVIEW
st.markdown("## Source Data Preview (ml_trading_data.csv)")
st.dataframe(df_raw.head(5), use_container_width=True)

# Footer
st.success(f"Data successfully loaded from GitHub — {file_used}")
