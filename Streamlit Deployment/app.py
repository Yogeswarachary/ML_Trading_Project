import streamlit as st
import pandas as pd
import os
from datetime import datetime
import matplotlib.pyplot as plt

st.set_page_config(page_title="ML Alpha Trading Dashboard", layout="wide")

st.title("📈 ML Alpha Trading – Performance Dashboard")

base_path = r"C:\Users\myoge\Contacts\Regression Based Project"

# Try to locate trading_strategy_results.csv
csv_path = os.path.join(base_path, "trading_results.csv")

if not os.path.exists(csv_path):
    st.error("❌ trading_results.csv not found. Please run the trading notebooks first.")
    st.stop()

# Load the latest trading results
df = pd.read_csv(csv_path)

# Display dataframe preview
st.subheader("Raw Strategy Results (latest file)")
st.dataframe(df.head())

# Extract Sharpe and Win Rate columns (if available)
if "Sharpe" in df.columns:
    avg_sharpe = df["Sharpe"].mean()
    st.metric(label="Average Sharpe Ratio", value=f"{avg_sharpe:.3f}")


if "Win_Rate" in df.columns:
    avg_win = df["Win_Rate"].mean()
    st.metric(label="Average Win Rate (%)", value=f"{avg_win*100:.2f}%")

# If multiple daily CSVs exist in 'runs/', read them all to plot Sharpe trend
runs_path = os.path.join(base_path, "runs")

sharpe_trend = []

if os.path.exists(runs_path):
    for file in os.listdir(runs_path):
        if file.endswith(".csv") and "trading_results" in file:  # ← More flexible
            try:
                df_temp = pd.read_csv(os.path.join(runs_path, file))
                # Try different possible Sharpe column names
                sharpe_col = None
                for col in ['sharpe_gross', 'Sharpe', 'sharpe_net', 'Sharpe Ratio']:
                    if col in df_temp.columns:
                        sharpe_col = col
                        break
                
                if sharpe_col:
                    date_str = file.split("_")[-1].replace(".csv", "")
                    sharpe_trend.append({
                        "Date": date_str,
                        "Sharpe": df_temp[sharpe_col].mean()
                    })
            except Exception as e:
                st.warning(f"Skipping {file}: {e}")

if sharpe_trend:
    trend_df = pd.DataFrame(sharpe_trend).sort_values("Date")
    trend_df["Date"] = pd.to_datetime(trend_df["Date"])
    st.subheader("📊 Sharpe Ratio Trend Over Time")
    st.line_chart(trend_df.set_index("Date"))
else:
    st.info("No historical Sharpe CSVs found in runs/ folder yet.")

