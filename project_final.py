

import streamlit as st
import pandas as pd
import os

# --- Page Title ---
st.title("Delhi Air Pollution Analysis (2015–2020)")

# --- Debug: Show Files ---
st.write("**Files in directory:**", os.listdir("."))

# --- Load Data with Error Handling ---
try:
    df = pd.read_csv("city_day.csv", parse_dates=['Date'])
    st.success("Data loaded successfully!")
    
    # --- Show Data ---
    st.write("### Data Preview")
    st.dataframe(df.head())

    st.write("### Dataset Info")
    st.write(f"**Rows:** {len(df)} | **Columns:** {len(df.columns)}")
    st.write("**Columns:**", list(df.columns))
    st.write(f"**Date Range:** {df['Date'].min().date()} → {df['Date'].max().date()}")

except Exception as e:
    st.error(f"Error: {e}")
    st.info("Check: Is `city_day.csv` uploaded? Are column names correct?")
