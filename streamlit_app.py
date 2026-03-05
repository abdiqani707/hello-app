import streamlit as st
from streamlit_gsheets import GSheetsConnection
import folium
from streamlit_folium import folium_static

st.set_page_config(page_title="GIS Pro Dashboard", layout="wide")

st.title("🛰️ GIS Dashboard: Satellite View & Details")

try:
    # 1. Keen xogta
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0).dropna(subset=['Latitude', 'Longitude'])

    # 2. Map-ka Bilowgiisa (Hargeisa Center)
    m = folium.Map(location=[9.5624, 44.0670], zoom_start=12, control_scale=True)

    # 3. Ku dar Satellite View (Google Maps Satellite)
    google_satellite = folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Satellite View',
        overlay = False,
        control = True
    ).add_to(m)
    
    folium.TileLayer('openstreetmap', name='Normal View').add_to(m)

    # 4. Ku dar dhibic kasta (Markers) iyo xogtooda
    for i, row in df.iterrows():
        # Diyaarinta qoraalka marka dhibicda la riixo (Popup)
        halkan_xogta = f"""
        <b>Magaca:</b> {row['Magaca Cusub']}<br>
        <b>GIS NO:</b> {row['GIS NO']}<br>
        <b>Cabbirka:</b> {row['Cabbirka']}<br>
        <b>Degmada:</b> {row['Degmada']}<br>
        <b>Mulkiile:</b> {row['Mulkiile/Wakiil']}<br>
        <b>Telefoon:</b> {row['Telefoonka Cusub']}
        """
        
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(halkan_xogta, max_width=300),
            tooltip=row['Magaca Cusub'], # Magaca oo soo baxa markaad dul istaagto uun
            icon=folium.Icon(color="blue", icon="info-sign")
        ).add_to(m)

    # 5. Ku dar badhanka lakabyada (Layer Control)
    folium.LayerControl().add_to(m)

    # 6. Soo bandhig khariidadda
    folium_static(m, width=1200, height=600)

    st.divider()
    st.subheader("📋 Jadwalka Xogta")
    st.dataframe(df)

except Exception as e:
    st.error(f"Khalad: {e}")
