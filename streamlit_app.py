import streamlit as st
from streamlit_gsheets import GSheetsConnection
import folium
from streamlit_folium import folium_static
from folium.plugins import LocateControl
import pandas as pd

# 1. Habaynta Bogga
st.set_page_config(page_title="Hargeisa GIS Pro", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #f0f2f6; }
    div[data-testid="stMetricValue"] { font-size: 28px; color: #1f77b4; }
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

st.title("🏙️ Hargeisa Urban GIS & Analytics Dashboard")

try:
    # 2. Isku xidhka Google Sheets
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(ttl=0).dropna(subset=['Latitude', 'Longitude'])

    # 3. Qaybta Metrics (Xogta Kooban)
    col_a, col_b, col_c, col_d = st.columns(4)
    col_a.metric("Wadarta Hantida", len(df))
    col_b.metric("Degmooyinka", df['Degmada'].nunique())
    col_c.metric("Dhul-Banaanka", len(df[df['Nooca Hantida'] == 'Dhul-Banaan']))
    col_d.metric("Cabbirka ugu badan", df['Cabbirka'].mode()[0] if not df['Cabbirka'].empty else "N/A")

    st.divider()

    # 4. Search iyo Filter (Sidebar & Main)
    st.sidebar.header("⚙️ Filter & Control")
    search_term = st.text_input("🔍 Raadi Magac, GIS NO ama Degmo:", "")

    # Sifeeyaha Degmooyinka (Sidebar)
    all_districts = df['Degmada'].unique().tolist()
    selected_districts = st.sidebar.multiselect("Dooro Degmada:", all_districts, default=all_districts)

    # Filter Logic
    filtered_df = df[df['Degmada'].isin(selected_districts)]
    if search_term:
        filtered_df = filtered_df[
            filtered_df['Magaca Cusub'].astype(str).str.contains(search_term, case=False) | 
            filtered_df['GIS NO'].astype(str).str.contains(search_term, case=False)
        ]

    # 5. Khariidadda iyo Garaafka (Side-by-Side)
    map_col, chart_col = st.columns([2, 1])

    with map_col:
        st.subheader("🗺️ Interactive GIS Map")
        
        # Auto-Zoom Logic
        if len(filtered_df) == 1:
            start_lat, start_lon, zoom_val = filtered_df.iloc[0]['Latitude'], filtered_df.iloc[0]['Longitude'], 19
        else:
            start_lat, start_lon, zoom_val = 9.5624, 44.0670, 13

        m = folium.Map(location=[start_lat, start_lon], zoom_start=zoom_val, tiles=None)
        
        # Satellite & Street Layers
        folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Satellite View').add_to(m)
        folium.TileLayer('openstreetmap', name='Street View').add_to(m)
        LocateControl(fly_to=True).add_to(m)

        for i, row in filtered_df.iterrows():
            popup_content = f"<b>{row['Magaca Cusub']}</b><br>GIS: {row['GIS NO']}<br>Nooca: {row['Nooca Hantida']}"
            folium.Marker(
                location=[row['Latitude'], row['Longitude']],
                popup=folium.Popup(popup_content, max_width=200),
                tooltip=row['Magaca Cusub'],
                icon=folium.Icon(color="red" if len(filtered_df)==1 else "blue", icon="home")
            ).add_to(m)

        folium.LayerControl().add_to(m)
        # Isticmaalka 'key' si uu Auto-zoom u shaqeeyo mar kasta
        folium_static(m, width=850, height=500, key=f"map_{search_term}")

    with chart_col:
        st.subheader("📊 Hantida / Degmo")
        # Samee Bar Chart muujinaya inta guri ee degmo kasta ku jirta
        district_counts = filtered_df['Degmada'].value_counts()
        st.bar_chart(district_counts)
        
        st.subheader("🏠 Nooca Hantida")
        type_counts = filtered_df['Nooca Hantida'].value_counts()
        st.write(type_counts)

    st.divider()

    # 6. Jadwalka iyo Download Button
    st.subheader("📋 Xogta Faahfaahsan")
    
    # Download Button (CSV)
    csv = filtered_df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Soo deji xogtan (CSV)",
        data=csv,
        file_name='Xogta_GIS_Hargeisa.csv',
        mime='text/csv',
    )
    
    st.dataframe(filtered_df, use_container_width=True)

except Exception as e:
    st.error(f"Khalad: {e}")
