import streamlit as st

# 1. Ciwaanka iyo Qoraalka (Headings and Text)
st.title('Interface-ka Streamlit')
st.header('Kusoo dhawaaw boggaaga cusub')
st.write('Kani waa tusaale ku saabsan sida loo isticmaalo buttons iyo input fields.')

# Khad kala qaybiya
st.divider()

# 2. Meelaha xogta laga geliyo (Input Fields)
st.subheader('Gali xogtaada hoos:')

magaca = st.text_input('Fadlan qor magacaaga:')
da'da = st.number_input('Immisa ayaad jirtaa?', min_value=1, max_value=100, value=18)

# 3. Badhamada (Buttons)
if st.button('Guji halkan si aad u gudbiso'):
    if magaca:
        st.success(f"Mahadsanid {magaca}! Xogtaada waa la helay.")
        st.info(f"Da'daada waa: {da'da}")
    else:
        st.warning("Fadlan magaca horta qor.")

# 4. Badhamada kale (Additional Buttons)
col1, col2 = st.columns(2)

with col1:
    if st.button('Haa'):
        st.write('Waad ku mahadsantahay dookhaaga Haa!')

with col2:
    if st.button('Maya'):
        st.write('Dhib maleh, Maya ayaad dooratay.')

# 5. Meel xog weyn laga qoro (Text Area)
faallo = st.text_area('Halkan ku qor faalladaada:')
