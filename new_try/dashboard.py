import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="IMD Combined Climate Console", layout="wide")
st.title("📈 5-Year Dual-Parameter Climate Analysis & ML Dataset Workspace")

@st.cache_data
def load_combined_database():
    df_master = pd.read_parquet("imd_combined_database")
    df_master["Date"] = pd.to_datetime(df_master["Date"])
    return df_master

try:
    df = load_combined_database()
except Exception as e:
    st.error("Could not find combined database. Run 'process_combined_5_years.py' successfully first!")
    st.stop()

# Sidebar selections
st.sidebar.header("🕹️ Parameters")
available_states = sorted(df["State"].unique())
selected_state = st.sidebar.selectbox("Choose State to Target:", available_states)

# Extract full 5-year data timeline slice for the selected region
state_df = df[df["State"] == selected_state].sort_values("Date")

# UI Visual Metrics Cards
st.subheader(f"⚡ 5-Year Integrated Analytics Summary: {selected_state}")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Total Rows Extracted", f"{len(state_df):,}")
m2.metric("Absolute Max Temperature", f"{state_df['Max_Temp'].max():.2f} °C")
m3.metric("Absolute Min Temperature", f"{state_df['Min_Temp'].min():.2f} °C")
m4.metric("Avg Diurnal Range", f"{(state_df['Max_Temp'] - state_df['Min_Temp']).mean():.2f} °C")

st.markdown("---")
col1, col2 = st.columns([4, 3])

with col1:
    st.subheader("📋 Machine Learning Feature Matrix")
    # Display the multi-variable data layout
    st.dataframe(state_df[["Date", "Latitude", "Longitude", "Max_Temp", "Min_Temp"]], use_container_width=True, height=350)

with col2:
    st.subheader("💡 Model Training Suitability Status")
    st.success(
        "Excellent! Your matrix is fully formatted for multi-variable forecasting models. "
        "You can now feed both Max_Temp and Min_Temp as features into an LSTM neural network "
        "or an Extreme Gradient Boosting (XGBoost) model to discover complex meteorological trends."
    )

# 5-Year Combined Time-Series Plotting
st.markdown("---")
st.subheader(f"📉 5-Year Chronological Max vs Min Temperature Fluctuations for {selected_state}")

# Compute daily macro-state averages for clean visualization lines
macro_timeline = state_df.groupby("Date")[["Max_Temp", "Min_Temp"]].mean().reset_index()

# Melt the dataframe format so Plotly can display two lines automatically
melted_timeline = pd.melt(macro_timeline, id_vars=["Date"], value_vars=["Max_Temp", "Min_Temp"], 
                          var_name="Parameter", value_name="Temperature")

fig_lines = px.line(
    melted_timeline, 
    x="Date", 
    y="Temperature", 
    color="Parameter",
    color_discrete_map={"Max_Temp": "#ef4444", "Min_Temp": "#3b82f6"}, # Red line for Max, blue line for Min
    title="Synchronous Daily Max & Min Microclimate Sequence (2021 - 2026)"
)
fig_lines.update_traces(line=dict(width=1))
st.plotly_chart(fig_lines, use_container_width=True)