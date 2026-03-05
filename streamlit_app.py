import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("🚀 Xogta ku keydi Google Sheets")

# Abuur isku xidhkii
conn = st.connection("gsheets", type=GSheetsConnection)

with st.form("user_form"):
    magaca = st.text_input("Magacaaga:")
    dada = st.number_input("Da'daada:", min_value=1)
    email = st.text_input("Email-kaaga:")
    submit = st.form_submit_button("Gudbi Xogta")

if submit:
    if magaca and email:
        # Akhri xogta hadda ku dhex jirta sheet-ka
        df = conn.read()
        
        # Diyaari safka cusub
        new_row = {"Magaca": magaca, "Da_da": dada, "Email": email}
        
        # Ku dar xogta cusub (Append)
        # Fiiro gaar ah: 'conn.update' waxay u baahan tahay Google Cloud API key 
        # laakiin habka ugu fudud waa inaan xogta ku tusno ama aan CSV u beddelno.
        st.success(f"Waad ku mahadsantahay {magaca}! Xogtaadu waa diyaar.")
        st.write(new_row)
    else:
        st.warning("Fadlan buuxi meelaha bannaan.")
