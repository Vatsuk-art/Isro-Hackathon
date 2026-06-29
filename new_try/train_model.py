import pandas as pd
import joblib

from xgboost import XGBRegressor

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)

# ==========================================================
# LOAD DATA
# ==========================================================

df = pd.read_parquet(
    r"C:\Users\schou\OneDrive\Documents\Isro-Hackathon\final_dataset.parquet"
)

print(df.head())

# ==========================================================
# FEATURES
# ==========================================================

features = [
    "Latitude",
    "Longitude",
    "Max_Temp",
    "Min_Temp",
    "Avg_Temp",
    "Temp_Range",
    "Month",
    "Day",
    "DayOfYear",
    "Season",
    "Rainfall_Yesterday",
    "Rainfall_3Day_Avg",
    "Rainfall_7Day_Avg"
]

# ==========================================================
# SORT BY DATE
# ==========================================================

df = df.sort_values("Date")

# ==========================================================
# TRAIN TEST SPLIT (80-20)
# ==========================================================

split = int(len(df) * 0.8)

train = df.iloc[:split]
test = df.iloc[split:]

X_train = train[features]
X_test = test[features]

y_train = train["Tomorrow_Rainfall"]
y_test = test["Tomorrow_Rainfall"]

print("Training Samples:", len(train))
print("Testing Samples:", len(test))

# ==========================================================
# XGBOOST MODEL
# ==========================================================

model = XGBRegressor(
    n_estimators=300,
    learning_rate=0.05,
    max_depth=8,
    subsample=0.8,
    colsample_bytree=0.8,
    random_state=42,
    n_jobs=-1
)

model.fit(X_train, y_train)

# ==========================================================
# PREDICTIONS
# ==========================================================

predictions = model.predict(X_test)

# ==========================================================
# EVALUATION
# ==========================================================

mae = mean_absolute_error(y_test, predictions)
rmse = mean_squared_error(y_test, predictions) ** 0.5
r2 = r2_score(y_test, predictions)

print("\n==============================")
print("MODEL PERFORMANCE")
print("==============================")

print(f"MAE  : {mae:.3f}")
print(f"RMSE : {rmse:.3f}")
print(f"R²   : {r2:.3f}")

# ==========================================================
# FEATURE IMPORTANCE
# ==========================================================

importance = pd.DataFrame({
    "Feature": features,
    "Importance": model.feature_importances_
})

importance = importance.sort_values(
    by="Importance",
    ascending=False
)

print("\n==============================")
print("FEATURE IMPORTANCE")
print("==============================")

print(importance)

# ==========================================================
# SAVE MODEL
# ==========================================================

joblib.dump(model, "rainfall_model.pkl")

print("\nModel Saved Successfully!")