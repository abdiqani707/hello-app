import streamlit as st
from streamlit_gsheets import GSheetsConnection
import folium
from streamlit_folium import st_folium
from folium.plugins import LocateControl, Draw, Geocoder
import pandas as pd
from datetime import datetime
import json
import base64
from PIL import Image
import io

# 1. Habaynta Bogga
st.set_page_config(page_title="Hargeisa GIS Pro", layout="wide")

# CSS si Menu-gu u noqdo mid qurux badan
st.markdown("""
    <style>
    [data-testid="stSidebar"] { background-color: #111d2b; color: white; }
    [data-testid="stSidebar"] * { color: white !important; }
    .stButton>button { width: 100%; border-radius: 5px; }
    </style>
    """, unsafe_allow_html=True)

# Function-ka Sawirka
def image_to_base64(image_file):
    if image_file is not None:
        img = Image.open(image_file)
        img.thumbnail((400, 400)) 
        buffered = io.BytesIO()
        img.save(buffered, format="JPEG")
        return base64.b64encode(buffered.getvalue()).decode()
    return ""

# --- LOGIN CHECK ---
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

# 2. Xidhiidhka Google Sheets
@st.cache_data(ttl=10)
def get_data():
    conn = st.connection("gsheets", type=GSheetsConnection)
    return conn.read(ttl=0)

df = get_data()

# --- SIDEBAR MENU ---
st.sidebar.image("https://cdn-icons-png.flaticon.com/512/854/854878.png", width=100)
st.sidebar.title("Hargeisa GIS Pro")
menu = st.sidebar.radio("DOORO QAYBTA:", ["🏠 Dashboard", "📝 Data Entry", "📊 Reports", "🔍 Search & Details"])
st.sidebar.divider()
if st.sidebar.button("Logout"):
    st.session_state["password_correct"] = False
    st.rerun()

# --- 1. DASHBOARD PAGE ---
if menu == "🏠 Dashboard":
    st.title("🏙️ Hargeisa Urban Dashboard")
    
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Wadarta Hantida", len(df))
    m2.metric("Degmooyinka", df['Degmada'].nunique())
    m3.metric("Diiwaangelinta Maanta", len(df[df['Taariikh'] == datetime.now().strftime("%Y-%m-%d")]))
    m4.metric("Noocyada Hantida", df['Nooca Hantida'].nunique())

    st.divider()
    
    col_map, col_chart = st.columns([2, 1])
    with col_map:
        st.subheader("🌐 Global Property Map")
        m = folium.Map(location=[9.5624, 44.0670], zoom_start=13)
        folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m)
        for _, row in df.dropna(subset=['Latitude', 'Longitude']).iterrows():
            folium.CircleMarker(
                location=[row['Latitude'], row['Longitude']],
                radius=5, color="red", fill=True, popup=row['Magaca Cusub']
            ).add_to(m)
        st_folium(m, width=800, height=450, key="dash_map")

    with col_chart:
        st.subheader("📈 Degmooyinka")
        st.bar_chart(df['Degmada'].value_counts())

# --- 2. DATA ENTRY PAGE ---
elif menu == "📝 Data Entry":
    st.title("📝 Diiwaangelinta Hanti Cusub")
    
    with st.expander("📍 DOORO GOOBTA KHARIIDADDA", expanded=True):
        m_entry = folium.Map(location=[9.5624, 44.0670], zoom_start=15)
        folium.TileLayer('https://mt1.google.com/vt/lyrs=s&x={x}&y={y}&z={z}', attr='Google', name='Satellite').add_to(m_entry)
        Draw().add_to(m_entry)
        LocateControl().add_to(m_entry)
        out = st_folium(m_entry, width=1100, height=400, key="entry_map")
        
        c_lat, c_lon, c_geo = 9.5624, 44.0670, ""
        if out.get("last_clicked"):
            c_lat, c_lon = out["last_clicked"]["lat"], out["last_clicked"]["lng"]
        if out.get("all_drawings"):
            c_geo = json.dumps(out["all_drawings"][-1])

    with st.form("master_form"):
        col1, col2, col3 = st.columns(3)
        with col1:
            f_magaca = st.text_input("Magaca Cusub:")
            f_mulkiile = st.selectbox("Mulkiile/Wakiil:", ["Mulkiile", "Wakiil", "Dowlada"])
            f_tel = st.text_input("Telefoonka Cusub:")
            f_gis = st.text_input("GIS NO:")
        with col2:
            f_cabbir = st.text_input("Cabbirka:")
            f_degmo = st.selectbox("Degmada:", ["Lixle", "Koodbuur", "SH.Bashiir", "F.Oomaar", "Gaacan-Libaax"])
            f_nooca = st.selectbox("Nooca Hantida:", ["Guri", "Dhul-Banaan", "Ganacsi", "Warshad"])
            f_foomka = st.selectbox("Nooca Foomka:", ["Cusub", "Bedel", "Cusboonaysiin"])
        with col3:
            f_looraace = st.text_input("Looraace:")
            f_magaca_hore = st.text_input("Magaca Hore:")
            f_waddo = st.text_input("Waddo:")
            f_comment = st.text_area("Comment:")

        st.divider()
        c_cam, c_up = st.columns(2)
        with c_cam: cam_file = st.camera_input("📷 Take Photo")
        with c_up: up_file = st.file_uploader("📁 Upload Image", type=['jpg','png'])
        
        final_img = cam_file if cam_file else up_file

        if st.form_submit_button("✅ KEYDI XOGTA"):
            img_str = image_to_base64(final_img)
            new_row = pd.DataFrame([{
                "Magaca Cusub": f_magaca, "Mulkiile/Wakiil": f_mulkiile, "Telefoonka Cusub": f_tel,
                "GIS NO": f_gis, "Cabbirka": f_cabbir, "Degmada": f_degmo, "Nooca Hantida": f_nooca,
                "Nooca Foomka": f_foomka, "Latitude": c_lat, "Longitude": c_lon, "Taariikh": datetime.now().strftime("%Y-%m-%d"),
                "Looraace": f_looraace, "Magaca Hore": f_magaca_hore, "Waddo": f_waddo, "Comment": f_comment,
                "Geoshape": c_geo, "Sawirka": img_str
            }])
            conn = st.connection("gsheets", type=GSheetsConnection)
            conn.update(data=pd.concat([df, new_row], ignore_index=True))
            st.success("Waa la keydiyey!")
            st.rerun()

# --- 3. REPORTS PAGE ---
elif menu == "📊 Reports":
    st.title("📊 Xogta iyo Warbixinnada")
    st.dataframe(df, use_container_width=True)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Soo deji CSV-ga Dhamaystiran", data=csv, file_name='GIS_Report.csv')

# --- 4. SEARCH & DETAILS PAGE ---
elif menu == "🔍 Search & Details":
    st.title("🔍 Baaritaan faahfaahsan")
    target = st.text_input("Geli Magac ama GIS NO si aad u aragto sawirka iyo xogta:")
    if target:
        res = df[df['Magaca Cusub'].str.contains(target, case=False, na=False) | df['GIS NO'].str.contains(target, case=False, na=False)]
        if not res.empty:
            for i, row in res.iterrows():
                c_info, c_img = st.columns([1, 1])
                with c_info:
                    st.write(f"**Magaca:** {row['Magaca Cusub']}")
                    st.write(f"**GIS NO:** {row['GIS NO']}")
                    st.write(f"**Degmada:** {row['Degmada']}")
                    st.write(f"**Coordinates:** {row['Latitude']}, {row['Longitude']}")
                with c_img:
                    if row['Sawirka']:
                        st.image(base64.b64decode(row['Sawirka']), width=300)
                st.divider()
