import streamlit as st, pandas as pd, json, folium
from streamlit_folium import st_folium
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
df=pd.read_parquet(ROOT/'final_dataset_cleaned.parquet')
with open(ROOT/'india_state_geo.json','r',encoding='utf-8') as f: geo=json.load(f)

df['Year']=pd.to_datetime(df['Date']).dt.year
year=st.sidebar.selectbox('Year',sorted(df['Year'].unique()))
sub=df[df['Year']==year]
state_stats=sub.groupby('State').agg(Rainfall_mm=('Rainfall_mm','sum'),Avg_Temp=('Avg_Temp','mean')).reset_index()
lookup=state_stats.set_index('State').to_dict('index')

for feat in geo['features']:
    name=feat['properties']['NAME_1']
    x=lookup.get(name,{})
    feat['properties']['rain']=round(x.get('Rainfall_mm',0),1)
    feat['properties']['temp']=round(x.get('Avg_Temp',0),1)

m=folium.Map(location=[22.5,78.9],zoom_start=5,tiles='CartoDB dark_matter')
folium.GeoJson(geo,style_function=lambda f:{'fillColor':'#0b5ed7','color':'#00e5ff','weight':1,'fillOpacity':0.55},tooltip=folium.GeoJsonTooltip(fields=['NAME_1','rain','temp'],aliases=['State','Annual Rainfall (mm)','Avg Temp (°C)'])).add_to(m)
st.title('🗺️ Interactive India Map')
st_folium(m,height=700,width=None)
