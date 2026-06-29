import joblib
import pandas as pd

# Load model
model = joblib.load("rainfall_model.pkl")

# Example input
sample = pd.DataFrame({
    "Latitude": [18.5],
    "Longitude": [81.5],
    "Max_Temp": [34],
    "Min_Temp": [24],
    "Avg_Temp": [(34 + 24) / 2],
    "Temp_Range": [34 - 24],
    "Month": [7],
    "Day": [15],
    "DayOfYear": [196],
    "Season": [2],
    "Rainfall_Yesterday": [12],
    "Rainfall_3Day_Avg": [8],
    "Rainfall_7Day_Avg": [10]
})

prediction = model.predict(sample)

print(f"Predicted Tomorrow's Rainfall: {prediction[0]:.2f} mm")