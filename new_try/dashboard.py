import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
import joblib

# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="ISRO Rainfall Prediction",
    layout="wide"
)

st.title("🌧️ ISRO Rainfall Prediction Dashboard")

st.write("Click anywhere on the map to predict tomorrow's rainfall.")

# ==========================================================
# LOAD MODEL
# ==========================================================

model = joblib.load(
    r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon\rainfall_model.pkl"
)

# ==========================================================
# LOAD DATASET
# ==========================================================

weather = pd.read_parquet(
    r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon\final_dataset.parquet"
)

# ==========================================================
# FIND NEAREST GRID
# ==========================================================

def get_nearest_location(lat, lon):

    temp = weather.copy()

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
    zoom_start=5
)

map_data = st_folium(
    india_map,
    width=900,
    height=500
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