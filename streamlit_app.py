import streamlit as st
from streamlit_gsheets import GSheetsConnection

st.title("Hubinta Isku-xidhka")

try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    # ttl=0 waxay ku qasbaysaa inuu hadda soo akhriyo xogta cusub
    df = conn.read(spreadsheet=st.secrets["connections"]["gsheets"]["spreadsheet"], ttl=0)
    
    if df.empty:
        st.warning("Sheet-ku waa furan yahay laakiin xog kuma jirto. Fadlan wax ku qor safka koowaad.")
    else:
        st.success("Xidhiidhku waa guul!")
        st.dataframe(df)
        
except Exception as e:
    st.error(f"Wali qalad ayaa jira: {e}")
    st.info("Talo: Hubi in safka koowaad ee Sheet-ka ay ku qoran yihiin 'Headers' (sida Magaca, Da'da).")
