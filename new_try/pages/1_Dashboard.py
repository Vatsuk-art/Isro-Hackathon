import pydeck as pdk
import plotly.express as px
import streamlit as st

from rainvision.data import (
    annual_region_summary,
    get_available_years,
    get_year_data,
    national_metrics,
)


st.set_page_config(layout="wide")

st.title("ISRO RainVision AI")
st.caption("Rainfall Intelligence Dashboard")

# ==================================================
# DATA
# ==================================================

years = get_available_years()

selected_year = st.sidebar.selectbox(
    "Select Year",
    years,
    index=len(years) - 1
)

df = get_year_data(selected_year)

summary = annual_region_summary(selected_year)

metrics = national_metrics(selected_year)

# ==================================================
# METRICS
# ==================================================

st.markdown("## Overview")

c1, c2, c3, c4 = st.columns(4, gap="large")

with c1:
    st.metric(
        "Total Rainfall",
        f"{metrics['total_rainfall']:,.0f} mm"
    )

with c2:
    st.metric(
        "Average Temperature",
        f"{metrics['avg_temp']:.1f} °C"
    )

with c3:
    st.metric(
        "Wettest Region",
        metrics["wettest_region"]
    )

with c4:
    st.metric(
        "Regions",
        metrics["regions"]
    )

st.divider()

# ==================================================
# LAYOUT
# ==================================================

left, center, right = st.columns(
    [1.2, 5, 1.5],
    gap="large"
)

# ==================================================
# LEFT PANEL
# ==================================================

with left:

    st.subheader("Mission Brief")

    st.write(
        """
        RainVision AI analyzes rainfall,
        temperature and climate patterns
        across India's major weather regions.
        """
    )

    st.metric(
        "Selected Year",
        selected_year
    )

# ==================================================
# MAP
# ==================================================

with center:

    st.subheader(
        f"India Rainfall Intensity Map • {selected_year}"
    )

    map_df = (
        df.groupby(
            ["Latitude", "Longitude", "State"],
            as_index=False
        )
        .agg(
            Rainfall_mm=("Rainfall_mm", "sum"),
            Avg_Temp=("Avg_Temp", "mean"),
        )
    )

    max_rain = map_df["Rainfall_mm"].max()

    map_df["radius"] = (
        map_df["Rainfall_mm"] / max_rain
        * 20000
    ).clip(
        lower=3000,
        upper=25000,
    )

    def color_mapper(x):

        ratio = x / max_rain

        if ratio > 0.8:
            return [255, 80, 80, 220]

        elif ratio > 0.6:
            return [255, 180, 50, 220]

        elif ratio > 0.4:
            return [220, 255, 50, 220]

        elif ratio > 0.2:
            return [50, 255, 180, 220]

        else:
            return [50, 180, 255, 220]

    map_df["color"] = map_df[
        "Rainfall_mm"
    ].apply(color_mapper)

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_df,

        get_position=["Longitude", "Latitude"],

        get_fill_color="color",

        get_radius="radius",

        pickable=True,

        auto_highlight=True,

        highlight_color=[
            255,
            255,
            255,
            255,
        ],

        stroked=True,

        get_line_color=[
            255,
            255,
            255,
        ],

        line_width_min_pixels=1,

        opacity=0.85,
    )

    view_state = pdk.ViewState(
        latitude=22.5,
        longitude=80,
        zoom=4,
        pitch=20,
    )

    tooltip = {
        "html": """
        <b>{State}</b><br/>
        Rainfall: {Rainfall_mm} mm<br/>
        Avg Temp: {Avg_Temp} °C
        """
    }

    st.pydeck_chart(
        pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip=tooltip,
            map_style="light",
        ),
        use_container_width=True,
    )

# ==================================================
# TOP REGIONS
# ==================================================

with right:

    st.subheader("Top 5 Regions")

    top5 = summary.head(5)

    for i, (_, row) in enumerate(top5.iterrows()):

        st.info(
            f"""
#{i+1} {row['State']}

Rainfall: {row['Annual_Rainfall']:,.0f} mm
"""
        )

st.divider()

# ==================================================
# BAR CHART
# ==================================================

st.subheader("Regional Rainfall Rankings")

fig = px.bar(
    summary,

    x="Annual_Rainfall",

    y="State",

    orientation="h",

    color="Annual_Rainfall",

    color_continuous_scale="Turbo",
)

fig.update_layout(
    height=700,

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font=dict(color="white"),

    yaxis=dict(
        categoryorder="total ascending"
    ),
)

st.plotly_chart(
    fig,
    use_container_width=True,
)

# ==================================================
# TABLE
# ==================================================

st.subheader("Regional Statistics")

st.dataframe(
    summary,
    use_container_width=True,
    hide_index=True,
)