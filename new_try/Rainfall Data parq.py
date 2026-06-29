import numpy as np
import pandas as pd
import os
from datetime import datetime, timedelta

# =========================
# SETTINGS
# =========================

folder = r"C:\Users\nandi\Downloads\IMD_Rainfall"

files = {
    2021: "Rainfall_ind2021_rfp25.grd",
    2022: "Rainfall_ind2022_rfp25.grd",
    2023: "Rainfall_ind2023_rfp25.grd",
    2024: "Rainfall_ind2024_rfp25.grd",
    2025: "Rainfall_ind2025_rfp25.grd"
}

ROWS = 129
COLS = 135

START_LAT = 6.5
START_LON = 66.5
STEP = 0.25

latitudes = [START_LAT + i * STEP for i in range(ROWS)]
longitudes = [START_LON + j * STEP for j in range(COLS)]

all_years = []

# =========================
# PROCESS FILES
# =========================

for year, filename in files.items():

    path = os.path.join(folder, filename)

    print(f"\nProcessing {filename}")

    days = 366 if year % 4 == 0 else 365

    with open(path, "rb") as f:

        for day in range(days):

            values = np.fromfile(
                f,
                dtype=np.float32,
                count=ROWS * COLS
            )

            if len(values) != ROWS * COLS:
                print(f"Stopped at day {day+1}")
                break

            grid = values.reshape(ROWS, COLS)

            date = datetime(year, 1, 1) + timedelta(days=day)

            rows = []

            for i in range(ROWS):
                for j in range(COLS):

                    rows.append({
                        "Date": date,
                        "Latitude": latitudes[i],
                        "Longitude": longitudes[j],
                        "Rainfall_mm": grid[i, j]
                    })

            all_years.append(pd.DataFrame(rows))

            if (day + 1) % 30 == 0:
                print(f"Completed {day+1} days")

# =========================
# SAVE PARQUET
# =========================

print("\nMerging data...")

master_df = pd.concat(all_years, ignore_index=True)

print(master_df.shape)

master_df.to_parquet(
    "imd_rainfall_2021_2025.parquet",
    engine="pyarrow",
    index=False
)

print("Parquet file created successfully!")