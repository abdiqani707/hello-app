import streamlit as st
from streamlit_gsheets import GSheetsConnection
import folium
from streamlit_folium import folium_static
from folium.plugins import LocateControl # Tan ayaa muhiim ah!

st.set_page_config(page_title="GIS Pro Dashboard", layout="wide")

st.title("🛰️ GIS Dashboard: Satellite & Live Location")

try:
    # 1. Keen xogta
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0).dropna(subset=['Latitude', 'Longitude'])

    # 2. Map-ka Bilowgiisa (Hargeisa Center)
    m = folium.Map(location=[9.5624, 44.0670], zoom_start=14, control_scale=True)

    # 3. Ku dar Satellite View
    folium.TileLayer(
        tiles = 'https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}',
        attr = 'Google',
        name = 'Satellite View',
        overlay = False,
        control = True
    ).add_to(m)
    
    folium.TileLayer('openstreetmap', name='Normal View').add_to(m)

    # 4. BADHANKA CURRENT LOCATION (GPS)
    # auto_start=True waxay ka dhigaysaa inuu isla markaaba ku raadiyo
    LocateControl(
        auto_start=False, 
        fly_to=True, 
        strings={"title": "Halkaan joogo ii sheeg", "popup": "Waxaad joogtaa halkan"}
    ).add_to(m)

    # 5. Ku dar dhibic kasta (Markers)
    for i, row in df.iterrows():
        halkan_xogta = f"""
        <div style="font-family: sans-serif; font-size: 14px;">
            <b>Magaca:</b> {row['Magaca Cusub']}<br>
            <b>GIS NO:</b> {row['GIS NO']}<br>
            <b>Cabbirka:</b> {row['Cabbirka']}<br>
            <b>Mulkiile:</b> {row['Mulkiile/Wakiil']}
        </div>
        """
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=folium.Popup(halkan_xogta, max_width=300),
            tooltip=row['Magaca Cusub'],
            icon=folium.Icon(color="blue", icon="home")
        ).add_to(m)

    # 6. Control Layers
    folium.LayerControl().add_to(m)

    # 7. Soo bandhig
    folium_static(m, width=1200, height=600)

except Exception as e:
    st.error(f"Khalad: {e}")
