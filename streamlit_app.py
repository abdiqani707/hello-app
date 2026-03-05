import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Hubinta Isku-xidhka")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # Isku day inaad akhrido xogta
    df = conn.read(ttl=0) # ttl=0 waxay ka dhigaysaa inaanu cache isticmaalin
    st.write("Xogta Sheet-kaaga:")
    st.dataframe(df)
except Exception as e:
    st.error(f"Wali qalad ayaa jira: {e}")
