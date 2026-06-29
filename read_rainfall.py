import pandas as pd
from pathlib import Path

# Full path to the rainfall parquet file
rainfall_file = Path(r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon\imd_rainfall_2021_2025.parquet")

# Read the file
df = pd.read_parquet(rainfall_file)

# Display information
print("=" * 50)
print("First 5 rows:")
print(df.head())

print("\n" + "=" * 50)
print("Columns:")
print(df.columns)

print("\n" + "=" * 50)
print("Info:")
print(df.info())

print("\n" + "=" * 50)
print("Shape:")
print(df.shape)

print("\n" + "=" * 50)
print("Missing Values:")
print(df.isnull().sum())