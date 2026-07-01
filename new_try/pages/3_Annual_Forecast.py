import streamlit as st, pandas as pd
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
df=pd.read_parquet(ROOT/'final_dataset_cleaned.parquet')
df['Date']=pd.to_datetime(df['Date'])
df['Year']=df['Date'].dt.year
st.title('📈 Analytics Dashboard')
col1,col2=st.columns(2)
with col1: st.subheader('Annual Rainfall'); st.line_chart(df.groupby('Year')['Rainfall_mm'].sum())
with col2: st.subheader('Monthly Rainfall'); st.bar_chart(df.groupby(df['Date'].dt.month)['Rainfall_mm'].mean())
st.subheader('Top 10 Wettest States')
st.bar_chart(df.groupby('State')['Rainfall_mm'].sum().sort_values(ascending=False).head(10))
st.subheader('Seasonal Rainfall')
st.bar_chart(df.groupby('Season')['Rainfall_mm'].mean())
