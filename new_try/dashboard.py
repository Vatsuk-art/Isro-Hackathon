import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# 1. Dashboard Layout Setups
st.set_page_config(page_title="5-Year IMD Climate Dashboard", layout="wide")
st.title("📈 5-Year IMD Temperature Analytics & ML Workspace")
st.markdown("This dashboard reads the multi-year consolidated Parquet database to present continuous timelines per state.")

# 2. Optimized Caching Loader
@st.cache_data
def load_five_year_db():
    # Automatically reads the nested Year and State sub-folders as a single table
    df_master = pd.read_parquet("imd_temperature_database")
    df_master["Date"] = pd.to_datetime(df_master["Date"])
    return df_master

try:
    df = load_five_year_db()
except Exception as e:
    st.error("Could not read 'imd_temperature_database'. Ensure you ran 'process_5_years.py' first.")
    st.stop()

# 3. Sidebar UI controls
st.sidebar.header("🕹️ Controls")
available_states = sorted(df["State"].unique())
selected_state = st.sidebar.selectbox("Choose State to Display:", available_states)

# Filter down to the full 5-year sequence of your selected state
state_5yr_df = df[df["State"] == selected_state].sort_values("Date")

# 4. KPI Summary Cards
st.subheader(f"⚡ Quick Statistics for {selected_state} (5-Year Historical Metrics)")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Data Points", f"{len(state_5yr_df):,}")
m2.metric("Record Max Temperature", f"{state_5yr_df['Temperature'].max():.2f} °C")
m3.metric("Record Min Temperature", f"{state_5yr_df['Temperature'].min():.2f} °C")
m4.metric("5-Year Average Temperature", f"{state_5yr_df['Temperature'].mean():.2f} °C")

# 5. Data Viewers
st.markdown("---")
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader(f"📋 Continuous Timeline Records: {selected_state}")
    st.dataframe(state_5yr_df[["Date", "Latitude", "Longitude", "Temperature"]], use_container_width=True, height=400)

with col2:
    st.subheader("💡 Ready for Time-Series Analysis")
    st.info(
        "The timeline table on the left presents data chronologically. "
        "You can feed this sequential structure directly into forecasting models "
        "(like ARIMA, Prophet, or LSTM) to predict future temperature spikes!"
    )
    
    # Simple station count visualizer to track stability of coordinates
    station_counts = state_5yr_df.groupby(["Latitude", "Longitude"]).size().reset_index(name="Days Tracked")
    st.write("Active Grid Tracking Points inside this State:")
    st.dataframe(station_counts, use_container_width=True, height=250)

# 6. Continuous 5-Year Time Series Plotting (Crucial for Forecasting Visibility)
st.markdown("---")
st.subheader(f"📉 5-Year Daily Average Temperature Fluctuations for {selected_state}")

# Group coordinates together to generate a clean, single regional average baseline sequence
daily_macro_timeline = state_5yr_df.groupby("Date")["Temperature"].mean().reset_index()

fig_line = px.line(
    daily_macro_timeline, 
    x="Date", 
    y="Temperature", 
    title="Continuous Daily Microclimate Sequence (2021 - 2025)",
    labels={"Temperature": "Mean State Temp (°C)"}
)
fig_line.update_traces(line=dict(color='#dc2626', width=1))
st.plotly_chart(fig_line, use_container_width=True)