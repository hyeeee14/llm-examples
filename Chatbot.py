import streamlit as st

st.caption("실험에 참여해주셔서 감사합니다!📝")
st.session_state["radio"] = st.radio("챗봇을 골라주세요!", ["chatbot_s", "chatbot_n"])

if st.session_state["radio"] == "chatbot_s":
    st.switch_page("pages/1_Chatbot-S.py")
else: 
    st.switch_page("pages/1_Chatbot-N.py")