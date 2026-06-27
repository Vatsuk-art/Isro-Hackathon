import os
from datetime import datetime, timedelta
import numpy as np
import pandas as pd

# --- CONFIGURE IMD GRID SETTINGS ---
ROWS, COLS = 31, 31
START_LAT = 37.5
START_LON = 67.5
GRID_STEP = 1.0


def get_state_from_coords(lat, lon):
    """Accurate rough-bounding box lookup for Indian regions."""
    if 32.0 <= lat <= 37.5 and 74.0 <= lon <= 80.0:
        return "Jammu & Kashmir / Ladakh"
    if 30.0 <= lat <= 32.5 and 74.0 <= lon <= 77.0:
        return "Punjab / Himachal"
    if 29.0 <= lat <= 31.5 and 77.0 <= lon <= 81.0:
        return "Uttarakhand / Haryana / Delhi"
    if 23.0 <= lat <= 30.0 and 69.0 <= lon <= 78.0:
        return "Rajasthan"
    if 24.0 <= lat <= 28.5 and 77.0 <= lon <= 84.0:
        return "Uttar Pradesh"
    if 21.0 <= lat <= 25.0 and 83.0 <= lon <= 88.0:
        return "Bihar / Jharkhand"
    if 20.0 <= lat <= 27.0 and 87.0 <= lon <= 93.0:
        return "West Bengal / Sikkim"
    if 21.0 <= lat <= 25.0 and 68.0 <= lon <= 74.5:
        return "Gujarat"
    if 21.0 <= lat <= 27.0 and 74.0 <= lon <= 83.0:
        return "Madhya Pradesh"
    if 19.5 <= lat <= 24.0 and 80.0 <= lon <= 85.0:
        return "Chhattisgarh"
    if 17.5 <= lat <= 22.5 and 82.0 <= lon <= 87.5:
        return "Odisha"
    if 15.5 <= lat <= 22.0 and 72.5 <= lon <= 81.0:
        return "Maharashtra"
    if 15.0 <= lat <= 19.5 and 79.0 <= lon <= 85.0:
        return "Andhra Pradesh"
    if 15.0 <= lat <= 19.0 and 77.0 <= lon <= 80.0:
        return "Telangana"
    if 11.5 <= lat <= 18.5 and 74.0 <= lon <= 78.5:
        return "Karnataka"
    if 8.0 <= lat <= 14.0 and 76.0 <= lon <= 80.5:
        return "Tamil Nadu"
    if 8.0 <= lat <= 13.0 and 74.5 <= lon <= 77.5:
        return "Kerala"
    if 22.0 <= lat <= 29.0 and 90.0 <= lon <= 97.5:
        return "North-East States"
    return "Other / Border Grid"


def append_year_to_db(file_path, year, output_dir="imd_temperature_database"):
    """Reads a full year GRD file, flattens, structures it, and saves it into the

    master partitioned folder.
    """
    is_leap = (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)
    total_days = 366 if is_leap else 365

    # Load whole year into a 3D block
    all_year_data = np.fromfile(file_path, dtype=np.float32).reshape(
        total_days, ROWS, COLS
    )

    start_date = datetime(year, 1, 1)
    records = []

    for day_idx in range(total_days):
        current_date = start_date + timedelta(days=day_idx)
        grid = all_year_data[day_idx, :, :]

        for i in range(ROWS):
            for j in range(COLS):
                temp_val = grid[i, j]
                if temp_val == 99.90:
                    continue

                lat = START_LAT - (i * GRID_STEP)
                lon = START_LON + (j * GRID_STEP)
                state_name = get_state_from_coords(lat, lon)

                records.append(
                    {
                        "Date": current_date,
                        "Latitude": lat,
                        "Longitude": lon,
                        "Temperature": temp_val,
                        "Year": year,  # Column used for folder structure partitioning
                        "State": state_name,  # Column used for folder structure partitioning
                    }
                )

    df = pd.DataFrame(records)
    # Save directly to the master directory (pandas handles adding new subfolders cleanly)
    df.to_parquet(
        output_dir, partition_cols=["Year", "State"], index=False, engine="pyarrow"
    )
    print(f"✅ Successfully processed and stored Year: {year}")


# --- MASTER BATCH CONFIGURATION ---
# Replace the file names below with the exact names of your 5 GRD files
dataset_files = {
    2021: "Maxtemp_MaxT_2021.GRD",
    2022: "Maxtemp_MaxT_2022.GRD",
    2023: "Maxtemp_MaxT_2023.GRD",
    2024: "Maxtemp_MaxT_2024.GRD",
    2025: "Maxtemp_MaxT_2025.GRD",  # Your current file
}

print("🚀 Launching 5-Year Data Engineering Pipeline...")
for year, filename in dataset_files.items():
    if os.path.exists(filename):
        append_year_to_db(filename, year)
    else:
        print(
            f"⚠️ File '{filename}' not found in directory. Skipping year {year}."
        )

print("\n🎉 Master Database Created! It contains all 5 years of processed data.")