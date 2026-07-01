from pathlib import Path

import pandas as pd


BASE_DIR = Path(__file__).resolve().parent.parent


def forecast_annual_rainfall(
    state_df,
    years_ahead=5,
):

    annual = (
        state_df
        .groupby("Year")
        .Rainfall_mm
        .sum()
        .reset_index()
    )

    annual.columns = [
        "Year",
        "Annual_Rainfall"
    ]

    # Make absolutely sure Year is numeric
    annual["Year"] = annual["Year"].astype(int)

    rolling_mean = (
        annual["Annual_Rainfall"]
        .tail(5)
        .mean()
    )

    trend = (
        annual["Annual_Rainfall"]
        .diff()
        .fillna(0)
        .mean()
    )

    last_year = int(
        annual["Year"].max()
    )

    forecasts = []

    for i in range(years_ahead):

        forecasts.append(
            {
                "Year": int(last_year + i + 1),

                "Predicted_Rainfall": round(
                    max(
                        rolling_mean + trend * i,
                        0
                    ),
                    2
                )
            }
        )

    return pd.DataFrame(forecasts)