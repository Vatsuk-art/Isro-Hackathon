import streamlit as st
import folium
from streamlit_folium import st_folium
import joblib
import pandas as pd
from pathlib import Path

# ----------------------------------------------------
# PROJECT FOLDER
# ----------------------------------------------------

PROJECT_FOLDER = Path(__file__).resolve().parent.parent

# ----------------------------------------------------
# PAGE SETTINGS
# ----------------------------------------------------

st.set_page_config(
    page_title="ISRO Rainfall Prediction",
    layout="wide"
)

st.title("🌧️ ISRO Rainfall Prediction Dashboard")

# ----------------------------------------------------
# LOAD MODEL
# ----------------------------------------------------

model = joblib.load(PROJECT_FOLDER / "rainfall_model.pkl")

# ==========================================================
# LOAD DATASET
# ==========================================================

weather = pd.read_parquet(
    r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon\final_dataset.parquet"
)

# ==========================================================
# YEAR + DATE FILTERS
# ==========================================================
# ==========================================================
# YEAR + DATE FILTERS
# ==========================================================

weather["Year"] = weather["Date"].dt.year

# Sidebar heading
st.sidebar.header("📅 Historical Data Filters")

# Select Year
selected_year = st.sidebar.selectbox(
    "Select Year",
    sorted(weather["Year"].unique())
)

# Filter dates for the selected year
available_dates = (
    weather.loc[weather["Year"] == selected_year, "Date"]
    .dt.date
    .sort_values()
    .unique()
)

# Select Date
selected_date = st.sidebar.selectbox(
    "Select Date",
    available_dates
)

# Display current selection
st.sidebar.success(
    f"Viewing data for: {selected_date}"
)

# Filter the dataset for the selected date
weather_filtered = weather[
    weather["Date"].dt.date == selected_date
]

# ==========================================================
# FIND NEAREST GRID
# ==========================================================


def get_nearest_location(lat, lon):

    temp = weather_filtered.copy()

    temp["distance"] = (
        (temp["Latitude"] - lat) ** 2 +
        (temp["Longitude"] - lon) ** 2
    )

    nearest = temp.loc[temp["distance"].idxmin()]

    return nearest


# ==========================================================
# CREATE MAP
# ==========================================================

india_map = folium.Map(
    location=[22.5, 78.9],
    zoom_start=5,
    tiles="CartoDB Positron"
)

# If the user has already clicked once, redraw the markers
if "last_clicked" in st.session_state:

    click = st.session_state["last_clicked"]

    folium.Marker(
        [click["lat"], click["lon"]],
        tooltip="📍 Selected Location",
        icon=folium.Icon(color="red")
    ).add_to(india_map)

    if "nearest" in st.session_state:

        n = st.session_state["nearest"]

        folium.Marker(
            [n["Latitude"], n["Longitude"]],
            tooltip="🟢 Nearest Weather Grid",
            icon=folium.Icon(color="green")
        ).add_to(india_map)

# Display the map
map_data = st_folium(
    india_map,
    width=900,
    height=500,
    key="india_map"
)
# ==========================================================
# WHEN USER CLICKS
# ==========================================================

if map_data["last_clicked"] is not None:

    lat = map_data["last_clicked"]["lat"]
    lon = map_data["last_clicked"]["lng"]

    st.success("📍 Location Selected")

    st.write(f"Latitude : {lat:.4f}")
    st.write(f"Longitude : {lon:.4f}")

    nearest = get_nearest_location(lat, lon)

    # Save clicked point and nearest grid
    st.session_state["last_clicked"] = {
        "lat": lat,
        "lon": lon
    }

    st.session_state["nearest"] = nearest

    # Historical records for this location
    location_history = weather[
        (weather["Latitude"] == nearest["Latitude"]) &
        (weather["Longitude"] == nearest["Longitude"]) &
        (weather["Year"] == selected_year)
    ].sort_values("Date")

    st.divider()

    st.subheader("Nearest Historical Weather Data")

    col1, col2 = st.columns(2)

    with col1:

        st.write("**State**")
        st.write(nearest["State"])

        st.write("**Date**")
        st.write(nearest["Date"])

        st.write("**Maximum Temperature**")
        st.write(f"{nearest['Max_Temp']:.2f} °C")

        st.write("**Minimum Temperature**")
        st.write(f"{nearest['Min_Temp']:.2f} °C")

    with col2:

        st.write("**Rainfall Yesterday**")
        st.write(f"{nearest['Rainfall_Yesterday']:.2f} mm")

        st.write("**3 Day Average Rainfall**")
        st.write(f"{nearest['Rainfall_3Day_Avg']:.2f} mm")

        st.write("**7 Day Average Rainfall**")
        st.write(f"{nearest['Rainfall_7Day_Avg']:.2f} mm")

    st.divider()

    st.subheader("📈 Rainfall Trend")

    chart_data = location_history.set_index("Date")["Rainfall_mm"]
    st.line_chart(chart_data)

    st.subheader("🌡 Temperature Trend")

    temp_chart = location_history.set_index("Date")[["Max_Temp", "Min_Temp"]]
    st.line_chart(temp_chart)

    st.subheader("🌧 Monthly Rainfall")

    monthly_rain = (
        location_history
        .groupby(location_history["Date"].dt.month)["Rainfall_mm"]
        .sum()
    )

    st.bar_chart(monthly_rain)

    if st.button("🌧 Predict Tomorrow's Rainfall"):

        sample = pd.DataFrame({

            "Latitude": [nearest["Latitude"]],
            "Longitude": [nearest["Longitude"]],

            "Max_Temp": [nearest["Max_Temp"]],
            "Min_Temp": [nearest["Min_Temp"]],

            "Avg_Temp": [nearest["Avg_Temp"]],
            "Temp_Range": [nearest["Temp_Range"]],

            "Month": [nearest["Month"]],
            "Day": [nearest["Day"]],
            "DayOfYear": [nearest["DayOfYear"]],

            "Season": [nearest["Season"]],

            "Rainfall_Yesterday": [nearest["Rainfall_Yesterday"]],
            "Rainfall_3Day_Avg": [nearest["Rainfall_3Day_Avg"]],
            "Rainfall_7Day_Avg": [nearest["Rainfall_7Day_Avg"]]

        })

        prediction = model.predict(sample)[0]

        st.divider()

        st.metric(
            label="🌧 Predicted Rainfall Tomorrow",
            value=f"{prediction:.2f} mm"
        )

        if prediction < 10:
            st.success("🟢 Low Rainfall Expected")
        elif prediction < 30:
            st.warning("🟡 Moderate Rainfall Expected")
        else:
            st.error("🔴 Heavy Rainfall Expected")

else:

    st.info("👆 Click on the map to begin.")