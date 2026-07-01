# rainvision/styles.py

import streamlit as st


def metric_card(title, value):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-value">{value}</div>
            <div class="metric-label">{title}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def glass_card(title, content):
    st.markdown(
        f"""
        <div class="glass-card">
            <h3>{title}</h3>
            <p>{content}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )