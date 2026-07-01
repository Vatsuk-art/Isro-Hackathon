# rainvision/mapping.py

import json
from pathlib import Path

import streamlit as st


GEOJSON_PATH = Path("india_state_geo(2).json")


# --------------------------------------------------
# Explicit state-name mappings
# GeoJSON NAME_1 -> Dataset State
# --------------------------------------------------

STATE_MAPPING = {
    "Andaman and Nicobar": "Andaman and Nicobar Islands",
    "Arunachal Pradesh": "Arunachal Pradesh",
    "Assam": "Assam",
    "Bihar": "Bihar",
    "Chandigarh": "Chandigarh",
    "Chhattisgarh": "Chhattisgarh",
    "Dadra and Nagar Haveli": "Dadra and Nagar Haveli and Daman and Diu",
    "Daman and Diu": "Dadra and Nagar Haveli and Daman and Diu",
    "Delhi": "Delhi",
    "Goa": "Goa",
    "Gujarat": "Gujarat",
    "Haryana": "Haryana",
    "Himachal Pradesh": "Himachal Pradesh",
    "Jammu and Kashmir": "Jammu and Kashmir",
    "Jharkhand": "Jharkhand",
    "Karnataka": "Karnataka",
    "Kerala": "Kerala",
    "Ladakh": "Ladakh",
    "Lakshadweep": "Lakshadweep",
    "Madhya Pradesh": "Madhya Pradesh",
    "Maharashtra": "Maharashtra",
    "Manipur": "Manipur",
    "Meghalaya": "Meghalaya",
    "Mizoram": "Mizoram",
    "Nagaland": "Nagaland",
    "Odisha": "Odisha",
    "Orissa": "Odisha",
    "Punjab": "Punjab",
    "Rajasthan": "Rajasthan",
    "Sikkim": "Sikkim",
    "Tamil Nadu": "Tamil Nadu",
    "Telangana": "Telangana",
    "Tripura": "Tripura",
    "Uttar Pradesh": "Uttar Pradesh",
    "Uttarakhand": "Uttarakhand",
    "Uttaranchal": "Uttarakhand",
    "West Bengal": "West Bengal",
}


# --------------------------------------------------
# Normalization
# --------------------------------------------------

def normalize_state_name(name: str) -> str:
    """
    Standardize state names before matching.
    """

    if name is None:
        return ""

    name = str(name).strip()

    replacements = {
        "&": "and",
        "NCT of Delhi": "Delhi",
        "Orissa": "Odisha",
        "Uttaranchal": "Uttarakhand",
    }

    for old, new in replacements.items():
        name = name.replace(old, new)

    return " ".join(name.split())


def dataset_name_from_geo(geo_name: str) -> str:
    """
    Convert GeoJSON state names
    into dataset names.
    """

    geo_name = normalize_state_name(geo_name)

    if geo_name in STATE_MAPPING:
        return STATE_MAPPING[geo_name]

    return geo_name


def geo_name_from_dataset(dataset_name: str) -> str:
    """
    Reverse lookup.
    """

    dataset_name = normalize_state_name(dataset_name)

    reverse_map = {
        v: k
        for k, v in STATE_MAPPING.items()
    }

    return reverse_map.get(
        dataset_name,
        dataset_name
    )


# --------------------------------------------------
# GeoJSON loading
# --------------------------------------------------

@st.cache_data(show_spinner=False)
def load_geojson():
    """
    Load India state boundaries.
    """

    with open(
        GEOJSON_PATH,
        "r",
        encoding="utf-8"
    ) as f:

        geo = json.load(f)

    return geo


@st.cache_data(show_spinner=False)
def get_geo_state_names():
    geo = load_geojson()

    names = []

    for feature in geo["features"]:
        names.append(
            feature["properties"]["NAME_1"]
        )

    return sorted(names)


# --------------------------------------------------
# Attach rainfall values to GeoJSON
# --------------------------------------------------

def enrich_geojson_with_rainfall(
    geojson: dict,
    rainfall_lookup: dict,
    temp_lookup: dict | None = None,
):
    """
    Adds annual rainfall and temperature
    directly into GeoJSON properties.

    Prevents state-name mismatch issues.
    """

    temp_lookup = temp_lookup or {}

    for feature in geojson["features"]:

        geo_name = feature["properties"]["NAME_1"]

        dataset_name = dataset_name_from_geo(
            geo_name
        )

        rainfall = rainfall_lookup.get(
            dataset_name,
            0,
        )

        temperature = temp_lookup.get(
            dataset_name,
            0,
        )

        feature["properties"][
            "mapped_state"
        ] = dataset_name

        feature["properties"][
            "annual_rainfall"
        ] = float(rainfall)

        feature["properties"][
            "avg_temperature"
        ] = float(temperature)

    return geojson


# --------------------------------------------------
# Diagnostics
# --------------------------------------------------

def find_unmatched_states(dataset_states):
    """
    Debug helper.

    Returns dataset states that
    have no GeoJSON mapping.
    """

    geo_states = {
        dataset_name_from_geo(x)
        for x in get_geo_state_names()
    }

    unmatched = sorted(
        set(dataset_states) - geo_states
    )

    return unmatched