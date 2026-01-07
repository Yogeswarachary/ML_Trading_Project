import streamlit as st
import pandas as pd
import glob
import os
import io
import requests

# DATA LAYER
@st.cache_data
def load_raw():
    """Loads the main ML trading dataset (CSV) directly from GitHub"""
    url = "https://raw.githubusercontent.com/Yogeswarachary/ML_Trading_Project/main/CSV%20Data/ml_trading_data.csv"
    response = requests.get(url)
    response.raise_for_status() 
    
    df = pd.read_csv(io.StringIO(response.text))
    return df


@st.cache_data
def build_dataset():
    """Wrapper function to prepare data (extendable later)"""
    df = load_raw()
    return df


@st.cache_data
def load_latest_trading_results():
    """Load trading results CSV directly from GitHub"""
    url = "https://raw.githubusercontent.com/Yogeswarachary/ML_Trading_Project/main/streamlit%20deployment/trading_results.csv"
    response = requests.get(url)
    response.raise_for_status()
    df = pd.read_csv(io.StringIO(response.text))
    st.info("📂 Loaded trading_results.csv from GitHub")
    return df, "GitHub Remote"

    
    deployment_files = []
    for path in possible_paths:
        deployment_files.extend(glob.glob(path))
    
    if not deployment_files:
        st.error("""
        ❌ No `trading_results*.csv` found!
        **Please check one of these paths:**
        - `streamlit deployment/`
        - `streamlit deployement/`
        - project root
        """)
        st.stop()
    
    # Pick the latest file
    latest_file = max(deployment_files, key=os.path.getctime)
    st.info(f"Loaded latest file: **{os.path.basename(latest_file)}**")
    
    df = pd.read_csv(latest_file)
    return df, latest_file


# MAIN DASHBOARD
st.set_page_config(page_title="ML Alpha Trading Dashboard", layout="wide")
st.title("ML Alpha Trading – Performance Dashboard")

# Load the trading results
df_trades, file_used = load_latest_trading_results()

# KPI CARDS
st.markdown("## Strategy Performance KPIs")

latest_metrics = df_trades.iloc[0]  # Assuming summary metrics are in first row

col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("📈 Sharpe Ratio", f"{latest_metrics.get('sharpe', 0):.3f}")
with col2:
    st.metric("🏆 Win Rate", f"{latest_metrics.get('win_rate', 0):.1%}")
with col3:
    st.metric("📉 Max Drawdown", f"{latest_metrics.get('max_dd', 0):.1%}")
with col4:
    st.metric("🔄 Turnover", f"{latest_metrics.get('turnover', 0):.1f}")

# RAW DATA PREVIEW
st.markdown("## Raw Strategy Results")
st.dataframe(
    df_trades.head(5),
    use_container_width=True,
    hide_index=False
)

# SUMMARY TABLE
if len(df_trades) > 1:
    st.markdown("## 📈 Performance Summary")
    summary = df_trades.iloc[0][['sharpe', 'win_rate', 'max_dd', 'turnover']].round(4)
    st.dataframe(summary.to_frame("Latest"), use_container_width=True)
