# Chatbot.py

import streamlit as st

st.set_page_config(
    page_title="Choose a chatbot💬",
    page_icon="✅",
    layout="centered",
    initial_sidebar_state="collapsed"  # 'collapsed'로 설정하면 사이드바 접힌 상태로 시작
)

st.markdown("실험에 참여해주셔서 감사합니다!📝")
st.caption("챗봇🤖을 골라주세요.")

if st.button("Chatbot-S"):
    st.switch_page("pages/1_Chatbot-S.py")
if st.button("Chatbot-N"):
    st.switch_page("pages/2_Chatbot-N.py")