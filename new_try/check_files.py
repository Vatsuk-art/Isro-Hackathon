from pathlib import Path

project = Path(r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon")

print("Searching for all parquet files...\n")

for file in project.rglob("*.parquet"):
    print(file)