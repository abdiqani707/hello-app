import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

# 1. Habaynta Bogga
st.set_page_config(page_title="GIS Dashboard", layout="wide")
st.title("📍 Khariidadda Goobaha GIS (Google Sheets)")

# 2. Isku xidhka Google Sheets
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # TTL=0 waxay ku qasbaysaa inuu soo qaado xogta ugu dambaysa ee Sheet-ka
    df = conn.read(ttl=0)
    
    # Nadiifinta: Iska tuur safaf banaan haddii ay jiraan
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # 3. Sidebar - Sifeeyaha Degmada
    st.sidebar.header("Sifee Xogta")
    degmooyin = df['Degmada'].unique().tolist()
    degmada_la_doonayo = st.sidebar.multiselect(
        "Dooro Degmada:",
        options=degmooyin,
        default=degmooyin
    )

    # Sifee xogta intaanan Map-ka saarin
    filtered_df = df[df['Degmada'].isin(degmada_la_doonayo)]

    # 4. Khariidadda (Map)
    st.subheader(f"🗺️ Khariidadda Degmooyinka: {', '.join(degmada_la_doonayo)}")
    
    if not filtered_df.empty:
        # Halkan waxaan ku sheegaynaa tiirarka saxda ah ee xogtaada ku jira
        st.map(filtered_df, latitude='Latitude', longitude='Longitude')
        
        st.divider()

        # 5. Jadwalka Xogta
        st.subheader("📋 Faahfaahinta Xogta la sifeeyey")
        st.dataframe(filtered_df, use_container_width=True)
    else:
        st.warning("Ma jirto xog laga helay degmada aad dooratay.")

except Exception as e:
    st.error(f"Xidhiidhka Google Sheets waa la diiday: {e}")
    st.info("Hubi in 'secrets.toml' uu sax yahay oo Sheet-ku yahay 'Anyone with the link'.")
