from pathlib import Path
from urllib.parse import unquote

import pandas as pd
import streamlit as st


BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "final_dataset_cleaned(2).parquet"


@st.cache_data
def load_data():

    df = pd.read_parquet(DATA_PATH)

    df["Date"] = pd.to_datetime(df["Date"])

    # Decode URL-encoded region names
    df["State"] = (
        df["State"]
        .astype(str)
        .apply(unquote)
        .str.strip()
    )

    return df


@st.cache_data
def get_available_years():
    df = load_data()
    return sorted(df["Year"].unique())


@st.cache_data
def get_available_states():
    df = load_data()
    return sorted(df["State"].unique())


def get_year_data(year):
    df = load_data()
    return df[df["Year"] == year]


def get_state_data(state):
    df = load_data()
    return df[df["State"] == state]


def yearly_state_summary(state):

    df = get_state_data(state)

    yearly = (
        df.groupby("Year")
        .agg(
            Annual_Rainfall=("Rainfall_mm", "sum"),
            Avg_Temp=("Avg_Temp", "mean"),
        )
        .reset_index()
    )

    return yearly


def monthly_state_summary(state):

    df = get_state_data(state)

    monthly = (
        df.groupby(["Year", "Month"])
        .agg(
            Rainfall=("Rainfall_mm", "sum"),
            Avg_Temp=("Avg_Temp", "mean"),
        )
        .reset_index()
    )

    return monthly


def national_annual_summary():

    df = load_data()

    return (
        df.groupby("Year")
        .agg(
            Total_Rainfall=("Rainfall_mm", "sum"),
            Avg_Temp=("Avg_Temp", "mean"),
        )
        .reset_index()
    )


def monthly_heatmap_data():

    df = load_data()

    pivot = (
        df.groupby(["State", "Month"])
        .Rainfall_mm.sum()
        .unstack(fill_value=0)
    )

    return pivot


def seasonal_summary():

    df = load_data()

    return (
        df.groupby(["State", "Season"])
        .agg(
            Rainfall=("Rainfall_mm", "sum"),
            Avg_Temp=("Avg_Temp", "mean"),
        )
        .reset_index()
    )


def annual_region_summary(year):

    df = get_year_data(year)

    return (
        df.groupby("State")
        .agg(
            Annual_Rainfall=("Rainfall_mm", "sum"),
            Avg_Temp=("Avg_Temp", "mean"),
        )
        .reset_index()
        .sort_values(
            "Annual_Rainfall",
            ascending=False
        )
    )


def national_metrics(year):

    summary = annual_region_summary(year)

    return {
        "total_rainfall":
            summary["Annual_Rainfall"].sum(),

        "avg_temp":
            summary["Avg_Temp"].mean(),

        "wettest_region":
            summary.iloc[0]["State"],

        "regions":
            len(summary),
    }