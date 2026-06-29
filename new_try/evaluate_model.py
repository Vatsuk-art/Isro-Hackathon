import pandas as pd
import joblib
import matplotlib.pyplot as plt

from sklearn.model_selection import train_test_split

df = pd.read_parquet(r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon\final_dataset.parquet")

X = df[
    [
        "Latitude",
        "Longitude",
        "Max_Temp",
        "Min_Temp",
        "Avg_Temp",
        "Temp_Range",
        "Month",
        "Day",
        "DayOfYear",
        "Season"
    ]
]

y = df["Rainfall_mm"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y,
    test_size=0.2,
    random_state=42
)

model = joblib.load("rainfall_model.pkl")

pred = model.predict(X_test)

plt.figure(figsize=(8,8))
plt.scatter(y_test, pred, alpha=0.2)
plt.xlabel("Actual Rainfall")
plt.ylabel("Predicted Rainfall")
plt.title("Actual vs Predicted Rainfall")
plt.grid(True)
plt.show()