# pages/2_Analytics.py

import calendar

import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from rainvision.data import (
    get_available_states,
    monthly_heatmap_data,
    monthly_state_summary,
    national_annual_summary,
    seasonal_summary,
)


st.title("Climate Analytics Center")

states = get_available_states()

selected_state = st.selectbox(
    "Select State",
    states,
)

# ==================================================
# MONTHLY RAINFALL TRENDS
# ==================================================

st.subheader("Monthly Rainfall Trends")

monthly = monthly_state_summary(selected_state)

monthly["Month_Name"] = monthly["Month"].apply(
    lambda x: calendar.month_abbr[int(x)]
)

fig_monthly = px.line(
    monthly,
    x="Month_Name",
    y="Rainfall",
    color="Year",
    markers=True,
    title=f"Monthly Rainfall Pattern • {selected_state}",
)

fig_monthly.update_layout(
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    legend_title="Year",
)

st.plotly_chart(
    fig_monthly,
    use_container_width=True,
)

# ==================================================
# NATIONAL ANNUAL TRENDS
# ==================================================

st.subheader("India Annual Rainfall Trends")

annual = national_annual_summary()

fig_annual = go.Figure()

fig_annual.add_trace(
    go.Scatter(
        x=annual["Year"],
        y=annual["Total_Rainfall"],
        mode="lines+markers",
        name="Rainfall",
    )
)

fig_annual.update_layout(
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    xaxis_title="Year",
    yaxis_title="Total Rainfall (mm)",
)

st.plotly_chart(
    fig_annual,
    use_container_width=True,
)

# ==================================================
# HEATMAP
# ==================================================

st.subheader("State × Month Rainfall Heatmap")

heatmap_df = monthly_heatmap_data()

month_labels = [
    calendar.month_abbr[i]
    for i in heatmap_df.columns
]

fig_heat = px.imshow(
    heatmap_df.values,
    labels=dict(
        x="Month",
        y="State",
        color="Rainfall (mm)"
    ),
    x=month_labels,
    y=heatmap_df.index,
    aspect="auto",
    color_continuous_scale="Turbo",
)

fig_heat.update_layout(
    height=900,
    paper_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
)

st.plotly_chart(
    fig_heat,
    use_container_width=True,
)

# ==================================================
# SEASONAL COMPARISON
# ==================================================

st.subheader("Seasonal Rainfall Comparison")

season_df = seasonal_summary()

state_season = season_df[
    season_df["State"] == selected_state
]

fig_season = px.bar(
    state_season,
    x="Season",
    y="Rainfall",
    color="Season",
    title=f"Seasonal Rainfall • {selected_state}",
)

fig_season.update_layout(
    height=500,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    showlegend=False,
)

st.plotly_chart(
    fig_season,
    use_container_width=True,
)

# ==================================================
# STATE RANKINGS
# ==================================================

st.subheader("Top Rainfall States")

ranking = (
    season_df
    .groupby("State")["Rainfall"]
    .sum()
    .reset_index()
    .sort_values(
        "Rainfall",
        ascending=False,
    )
    .head(15)
)

fig_rank = px.bar(
    ranking,
    x="Rainfall",
    y="State",
    orientation="h",
    title="Top 15 States by Historical Rainfall",
)

fig_rank.update_layout(
    height=700,
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(color="white"),
    yaxis=dict(categoryorder="total ascending"),
)

st.plotly_chart(
    fig_rank,
    use_container_width=True,
)