import streamlit as st

# 1. Ciwaanka Bogga (Page Config)
st.set_page_config(page_title="App-kayga Streamlit", page_icon="🚀")

# 2. Qaybta Sare (Header Section)
st.title('🚀 Streamlit App-kaaga Koowaad')
st.markdown("""
Kani waa interface dhamaystiran oo leh:
* **Input Fields** (Qoraal iyo Lambar)
* **Buttons** (Badhamno Action leh)
* **File Uploader** (Meel sawir laga soo geliyo)
""")

st.divider()

# 3. Meelaha xogta laga geliyo (Input Section)
st.subheader('📝 Fadlan buuxi macluumaadkaaga')

# Halkan waxaan u isticmaalay 'dada' halkii aan ka isticmaali lahaa 'da'da' si khaladku u baxo
magaca = st.text_input('Magacaaga oo buuxa:', placeholder="Tusaale: Axmed Cali")
dada = st.number_input('Immisa ayaad jirtaa?', min_value=1, max_value=100, value=20)
email = st.text_input('Email-kaaga:', placeholder="example@mail.com")

# 4. Badhamada (Buttons)
col1, col2 = st.columns(2)

with col1:
    if st.button('✅ Gudbi Xogta'):
        if magaca and email:
            st.success(f"Waad ku mahadsantahay, {magaca}!")
            st.write(f"Xogtaada waa la keydiyay. Da'daadu waa {dada}.")
        else:
            st.error("Fadlan buuxi dhammaan meelaha bannaan.")

with col2:
    if st.button('🗑️ Masax Form-ka'):
        st.info("Fadlan refresh dheh page-ka si aad u masaxdo.")

st.divider()

# 5. Meel sawirka ama file-ka laga soo geliyo (File Uploader)
st.subheader('🖼️ Upload garee Sawir')
uploaded_file = st.file_uploader("Dooro sawir aad rabto inaan soo bandhigno", type=["jpg", "png", "jpeg"])

if uploaded_file is not None:
    st.image(uploaded_file, caption='Sawirka aad soo gelisay', use_container_width=True)

# 6. Sidebar (Dhinaca bidix)
st.sidebar.title("Settings")
st.sidebar.write("Halkan waa meel aad ku dari karto menu-yo dheeri ah.")
option = st.sidebar.selectbox(
    'Sidee ayaad u aragtaa app-kan?',
    ('Aad u fiican', 'Dhexdhexaad', 'Ma fiicna')
)

st.sidebar.write(f"Waad ku mahadsantahay ra'yigaaga: **{option}**")
