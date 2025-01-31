import streamlit as st

st.markdown(
    "<h3 style='text-align: center;'>실험에 참여해주셔서 감사합니다!📝</h1>",
    "<h1 style='text-align: center;'>챗봇🤖을 골라주세요. </h1>",
    unsafe_allow_html=True
)

st.markdown("실험에 참여해주셔서 감사합니다!📝")
st.caption("챗봇을 골라주세요.")

if st.button("Chatbot-S"):
    st.switch_page("pages/1_Chatbot-S.py")
if st.button("Chatbot-N"):
    st.switch_page("pages/2_Chatbot-N.py")