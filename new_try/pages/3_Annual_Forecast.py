import plotly.graph_objects as go
import streamlit as st

from rainvision.data import (
    get_available_states,
    get_state_data,
    yearly_state_summary,
)

from rainvision.forecasting import (
    forecast_annual_rainfall
)


st.title("Annual Rainfall Forecast Engine")

states = get_available_states()

selected_state = st.selectbox(
    "Region",
    states
)

years = st.slider(
    "Forecast Horizon",
    1,
    10,
    5
)


history = yearly_state_summary(
    selected_state
)

state_df = get_state_data(
    selected_state
)

forecast_df = forecast_annual_rainfall(
    state_df,
    years
)


fig = go.Figure()

fig.add_trace(
    go.Scatter(
        x=history["Year"],
        y=history["Annual_Rainfall"],
        mode="lines+markers",
        name="Historical"
    )
)

fig.add_trace(
    go.Scatter(
        x=forecast_df["Year"],
        y=forecast_df["Predicted_Rainfall"],
        mode="lines+markers",
        line=dict(dash="dash"),
        name="Forecast"
    )
)

fig.update_layout(
    height=700,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white")
)

st.plotly_chart(
    fig,
    use_container_width=True
)


st.subheader("Forecast Data")

st.dataframe(
    forecast_df,
    use_container_width=True
)


st.download_button(
    "Download CSV",
    forecast_df.to_csv(index=False),
    file_name=f"{selected_state}.csv",
    mime="text/csv"
)