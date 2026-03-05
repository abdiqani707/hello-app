import streamlit as st
import pandas as pd

# 1. Ciwaanka Bogga
st.set_page_config(page_title="Xogta GIS - Hargeisa", layout="wide")
st.title("📍 Khariidadda Goobaha GIS")

# 2. Akhrinta Xogta (Halkan waxaan u isticmaalay file-ka aad soo dirtay)
# Haddii aad Google Sheets isticmaalayso, isticmaal 'conn.read()' sidii hore
try:
    df = pd.read_csv('MAANTA.csv')
    
    # Nadiifinta xogta (Iska tuur safaf banaan haddii ay jiraan)
    df = df.dropna(subset=['Latitude', 'Longitude'])

    # 3. Soo bandhigista Khariidadda
    st.subheader("🗺️ Goobaha Khariidadda ku yaalla")
    
    # Streamlit wuxuu u baahan yahay inuu ogaado tiirarka loolka iyo dhigaha
    # Maadaama xogtaadu leedahay 'Latitude' iyo 'Longitude', halkan ayaan ku qeexaynaa
    st.map(df, latitude='Latitude', longitude='Longitude')

    st.divider()

    # 4. Jadwalka Xogta oo faahfaahsan
    st.subheader("📋 Liiska Xogta oo Dhamaystiran")
    
    # Waxaan dooranaynaa tiirarka muhiimka ah si ay u muuqdaan
    tiirarka_muhiimka_ah = [
        'Magaca Cusub', 'Degmada', 'GIS NO', 'Latitude', 'Longitude', 'Nooca Hantida'
    ]
    st.dataframe(df[tiirarka_muhiimka_ah], use_container_width=True)

except FileNotFoundError:
    st.error("File-kii 'MAANTA.csv' lama helin. Hubi inuu ku jiro isla folder-ka app-ka.")
except Exception as e:
    st.error(f"Cillad ayaa dhacday: {e}")

# 5. Sidebar-ka (Sifeeyaha/Filters)
st.sidebar.header("Sifee Xogta")
degmada_la_doonayo = st.sidebar.multiselect(
    "Dooro Degmada:",
    options=df['Degmada'].unique(),
    default=df['Degmada'].unique()
)

# Haddii qofku doorto degmo gaar ah, xogta u sifee
filtered_df = df[df['Degmada'].is_in(degmada_la_doonayo)]
