from pathlib import Path
import pandas as pd

project_folder = Path(__file__).parent
rain_folder = project_folder / "imd_combined_database"

parquet_files = list(rain_folder.rglob("*.parquet"))

print(f"Found {len(parquet_files)} parquet files")

dfs = []

for file in parquet_files:
    try:
        df = pd.read_parquet(file)

        # Extract Year and State from folder names
        year = file.parent.parent.name.replace("Year=", "")
        state = file.parent.name.replace("State=", "")

        df["Year"] = year
        df["State"] = state

        dfs.append(df)

        print(f"Loaded {state} ({year})")

    except Exception as e:
        print(file)
        print(e)

master_df = pd.concat(dfs, ignore_index=True)

print("\nFinal Shape:")
print(master_df.shape)

print("\nColumns:")
print(master_df.columns)

print("\nFirst Rows:")
print(master_df.head())

# Save for later use
master_df.to_parquet("master_weather.parquet", index=False)

print("\nSaved as master_weather.parquet")