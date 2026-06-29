import pandas as pd
df = pd.read_parquet("C:\\Users\\schou\\OneDrive\\Documents\\Isro-Hackathon\\final_dataset.parquet")
print(df.head())
print(df.columns)