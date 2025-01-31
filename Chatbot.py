import streamlit as st

st.session_state["radio"] = st.radio("Radio", ["chatbot_s", "chatbot_n"])

if st.session_state["radio"] == "chatbot_s":
    st.switch_page("pages/1_Chatbot-S.py")
else: 
    st.switch_page("pages/1_Chatbot-N.py")