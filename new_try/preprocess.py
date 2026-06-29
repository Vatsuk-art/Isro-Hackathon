import pandas as pd
import numpy as np
from pathlib import Path

# ==========================================================
# PROJECT FOLDER
# ==========================================================

project_folder = Path(r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon")

# ==========================================================
# LOAD TEMPERATURE DATA
# ==========================================================

temp_file = project_folder / "master_weather.parquet"

temperature = pd.read_parquet(temp_file)

print("=" * 60)
print("Temperature Dataset Loaded")
print(temperature.shape)
print(temperature.head())

# ==========================================================
# LOAD RAINFALL DATA
# ==========================================================

rain_file = project_folder / "imd_rainfall_2021_2025.parquet"

rainfall = pd.read_parquet(rain_file)

print("=" * 60)
print("Rainfall Dataset Loaded")
print(rainfall.shape)
print(rainfall.head())

# ==========================================================
# CHECK COLUMNS
# ==========================================================

print("\nTemperature Columns:")
print(temperature.columns)

print("\nRainfall Columns:")
print(rainfall.columns)

# ==========================================================
# CLEAN RAINFALL
# ==========================================================

rainfall["Rainfall_mm"] = rainfall["Rainfall_mm"].replace(-999, np.nan)

rainfall = rainfall.dropna()

print("=" * 60)
print("Rainfall After Cleaning")
print(rainfall.shape)

# ==========================================================
# DATE FORMAT
# ==========================================================

temperature["Date"] = pd.to_datetime(temperature["Date"])
rainfall["Date"] = pd.to_datetime(rainfall["Date"])

# ==========================================================
# MERGE
# ==========================================================

master = pd.merge(
    temperature,
    rainfall,
    on=["Date", "Latitude", "Longitude"],
    how="inner"
)

print("=" * 60)
print("Merged Dataset")
print(master.shape)
print(master.head())

# ==========================================================
# SORT DATA
# ==========================================================

master = master.sort_values(["Latitude", "Longitude", "Date"])

# ==========================================================
# CREATE TARGET (Tomorrow's Rainfall)
# ==========================================================

master["Tomorrow_Rainfall"] = (
    master.groupby(["Latitude", "Longitude"])["Rainfall_mm"].shift(-1)
)

# ==========================================================
# CREATE LAG FEATURES
# ==========================================================

master["Rainfall_Yesterday"] = (
    master.groupby(["Latitude", "Longitude"])["Rainfall_mm"].shift(1)
)

master["Rainfall_3Day_Avg"] = (
    master.groupby(["Latitude", "Longitude"])["Rainfall_mm"]
          .rolling(window=3)
          .mean()
          .reset_index(level=[0, 1], drop=True)
)

master["Rainfall_7Day_Avg"] = (
    master.groupby(["Latitude", "Longitude"])["Rainfall_mm"]
          .rolling(window=7)
          .mean()
          .reset_index(level=[0, 1], drop=True)
)

# Remove rows with missing values created by shifting/rolling
master = master.dropna()

print("=" * 60)
print("Lag Features Created")
print(master.shape)

# STOP HERE FIRST

# ==========================================================
# FEATURE ENGINEERING
# ==========================================================

master["Avg_Temp"] = (
    master["Max_Temp"] + master["Min_Temp"]
) / 2

master["Temp_Range"] = (
    master["Max_Temp"] - master["Min_Temp"]
)

master["Month"] = master["Date"].dt.month
master["Day"] = master["Date"].dt.day
master["DayOfYear"] = master["Date"].dt.dayofyear

# Seasons
def get_season(month):
    if month in [12, 1, 2]:
        return 0   # Winter
    elif month in [3, 4, 5]:
        return 1   # Summer
    elif month in [6, 7, 8, 9]:
        return 2   # Monsoon
    else:
        return 3   # Post Monsoon

master["Season"] = master["Month"].apply(get_season)

print("\nFeature Engineering Done!")

print(master.head())

print("\nFinal Dataset Columns:")
print(master.columns)

print("\nFinal Dataset Shape:")
print(master.shape)

master.to_parquet(
    project_folder / "final_dataset.parquet",
    index=False
)

print("Saved final_dataset.parquet") 