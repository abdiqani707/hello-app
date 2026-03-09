import streamlit as st
from streamlit_gsheets import GSheetsConnection
import folium
from streamlit_folium import st_folium
from folium.plugins import LocateControl, Draw, Geocoder, Fullscreen
import pandas as pd
import plotly.express as px
from datetime import datetime
import json
import base64
from PIL import Image
import io

# 1. Page Config
st.set_page_config(page_title="Hargeisa GIS Pro", layout="wide")

# Function sawirka
def image_to_base64(image_file):
    if image_file is not None:
        img = Image.open(image_file)
        img.thumbnail((400, 400)) 
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    return ""

# 2. LOGIN (Waa inuu horta yimaadaa)
if "password_correct" not in st.session_state:
    st.session_state["password_correct"] = False

if not st.session_state["password_correct"]:
    st.title("🔐 GIS System Login")
    u = st.text_input("Username")
    p = st.text_input("Password", type="password")
    if st.button("Log In"):
        if u == "admin" and p == "hargeisa2026":
            st.session_state["password_correct"] = True
            st.rerun()
        else:
            st.error("Username ama Password waa khalad!")
    st.stop()

# 3. CONNECTION & DATA
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read(ttl=0)

# 4. SIDEBAR MENU
with st.sidebar:
    st.title("🏙️ Hargeisa GIS")
    choice = st.radio("MENU:", ["🏠 Dashboard", "📝 Data Registration", "📊 Reports", "🔍 Search"])
    st.divider()
    if st.button("🔴 Logout"):
        st.session_state["password_correct"] = False
        st.rerun()

# --- 5. BOGGA DASHBOARD ---
if choice == "🏠 Dashboard":
    st.title("📊 Analytics & Overview")
    c1, c2, c3 = st.columns(3)
    c1.metric("Wadarta Hantida", len(df))
    c2.metric("Degmooyinka", df['Degmada'].nunique())
    c3.metric("Maanta", datetime.now().strftime("%d/%m/%Y"))
    
    st.divider()
    col_map, col_chart = st.columns([2, 1])
    with col_map:
        m = folium.Map(location=[9.5624, 44.0670], zoom_start=13)
        folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m)
        for _, row in df.dropna(subset=['Latitude', 'Longitude']).iterrows():
            folium.CircleMarker([row['Latitude'], row['Longitude']], radius=5, color="red", popup=row['Magaca Cusub']).add_to(m)
        st_folium(m, width=800, height=450, key="dash_map")
    with col_chart:
        fig = px.pie(df, names='Degmada', title="Hantida Degmooyinka")
        st.plotly_chart(fig, use_container_width=True)

# --- 6. BOGGA DATA REGISTRATION (Kan aad khaladka ka sheegtay) ---
elif choice == "📝 Data Registration":
    st.title("📝 Diiwaangelin Cusub")
    
    # Map selection logic
    with st.expander("📍 CALAAMADI GOOBTA KHARIIDADDA", expanded=True):
        m_entry = folium.Map(location=[9.5624, 44.0670], zoom_start=15)
        folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m_entry)
        Draw().add_to(m_entry)
        output = st_folium(m_entry, width=1000, height=350, key="reg_map")
        
        c_lat, c_lon, c_geo = 9.5624, 44.0670, ""
        if output.get("last_clicked"):
            c_lat, c_lon = output["last_clicked"]["lat"], output["last_clicked"]["lng"]
        if output.get("all_drawings") and len(output["all_drawings"]) > 0:
            c_geo = json.dumps(output["all_drawings"][-1])

    # Form
    with st.form("master_form", clear_on_submit=True):
        st.write(f"📍 Coordinates: `{c_lat:.6f}, {c_lon:.6f}`")
        col1, col2 = st.columns(2)
        with col1:
            f_magaca = st.text_input("Magaca Cusub:")
            f_gis = st.text_input("GIS NO:")
            f_tel = st.text_input("Telefoonka:")
            f_degmo = st.selectbox("Degmada:", ["Lixle", "Koodbuur", "SH.Bashiir", "F.Oomaar", "Gaacan-Libaax"])
        with col2:
            f_cabbir = st.text_input("Cabbirka:")
            f_nooca = st.selectbox("Nooca Hantida:", ["Guri", "Dhul-Banaan", "Ganacsi", "Dawlad"])
            f_foomka = st.selectbox("Nooca Foomka:", ["Cusub", "Bedel", "Cusboonaysiin"])
            f_mulkiile = st.selectbox("Mulkiile/Wakiil:", ["Mulkiile", "Wakiil"])
        
        f_comment = st.text_area("Comment:")
        cam_file = st.camera_input("📷 Sawirka Hantida")
        
        if st.form_submit_button("✅ KEYDI XOGTA"):
            img_str = image_to_base64(cam_file)
            new_row = pd.DataFrame([{
                "Magaca Cusub": f_magaca, "Cabbirka": f_cabbir, "Degmada": f_degmo,
                "Mulkiile/Wakiil": f_mulkiile, "Telefoonka Cusub": f_tel, "GIS NO": f_gis,
                "Latitude": c_lat, "Longitude": c_lon, "Taariikh": datetime.now().strftime("%Y-%m-%d"),
                "Comment": f_comment, "Geoshape": c_geo, "Sawirka": img_str
            }])
            updated_df = pd.concat([df, new_row], ignore_index=True)
            conn.update(data=updated_df)
            st.success("Waa la keydiyey!")
            st.rerun()

# --- 7. BOGGA REPORTS ---
elif choice == "📊 Reports":
    st.title("📋 Jadwalka Xogta")
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name="GIS_Report.csv")

# --- 8. BOGGA SEARCH ---
elif choice == "🔍 Search":
    st.title("🔍 Baaritaan")
    q = st.text_input("Geli Magaca ama GIS NO:")
    if q:
        res = df[df['Magaca Cusub'].str.contains(q, case=False, na=False) | df['GIS NO'].str.contains(q, case=False, na=False)]
        st.table(res[['Magaca Cusub', 'GIS NO', 'Degmada', 'Cabbirka']])
        if not res.empty and res.iloc[0]['Sawirka']:
            st.image(base64.b64decode(res.iloc[0]['Sawirka']), caption=res.iloc[0]['Magaca Cusub'])
