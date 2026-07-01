# app.py

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="ISRO RainVision AI",
    page_icon="🌧️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# Load global stylesheet
# -----------------------------
css_path = Path("assets/custom.css")

if css_path.exists():
    with open(css_path, "r", encoding="utf-8") as f:
        st.markdown(
            f"<style>{f.read()}</style>",
            unsafe_allow_html=True,
        )

# -----------------------------
# Landing Hero
# -----------------------------
st.markdown(
    """
    <div class="hero-container">

        <div class="hero-badge">
            🇮🇳 ISRO HACKATHON 2026
        </div>

        <h1 class="hero-title">
            ISRO RainVision AI
        </h1>

        <p class="hero-subtitle">
            Advanced rainfall intelligence, climate analytics,
            and annual forecasting platform powered by geospatial AI.
        </p>

    </div>
    """,
    unsafe_allow_html=True,
)

col1, col2, col3 = st.columns([1.2, 1, 1.2])

with col1:
    st.markdown(
        """
        <div class="glass-card">
            <h3>🌧️ Dashboard</h3>

            <p>
            Explore India's rainfall patterns through an interactive
            geospatial intelligence interface.
            </p>

            <ul>
                <li>Interactive state map</li>
                <li>Annual rainfall metrics</li>
                <li>Temperature indicators</li>
                <li>Wettest-state rankings</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col2:
    st.markdown(
        """
        <div class="glass-card center-card">
            <div class="pulse-ring"></div>

            <h2>RAINVISION CORE</h2>

            <p>
            Unified climate analytics engine built on
            historical rainfall intelligence.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

with col3:
    st.markdown(
        """
        <div class="glass-card">
            <h3>📈 Forecast Engine</h3>

            <p>
            Annual rainfall forecasting using trained machine learning
            models and historical climate signals.
            </p>

            <ul>
                <li>Yearly predictions</li>
                <li>State-level insights</li>
                <li>Downloadable outputs</li>
                <li>Trend interpretation</li>
            </ul>
        </div>
        """,
        unsafe_allow_html=True,
    )

st.markdown("<br>", unsafe_allow_html=True)

st.info(
    "Use the left navigation panel to open Dashboard, Analytics, and Annual Forecast modules."
)