import streamlit as st

st.title("📝 Career Decision-making Difficulties Questionnaire")
st.text("총 10개의 질문으로 진로결정 어려움에 대해 측정합니다. by. GAti")

score_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_1 = st.radio('1. I know that I have to choose a career, but I don’t have the motivation to make the decision now (I don’t feel like it)', options = score_1)   

# Create Radio Buttons
st.radio(label = 'Radio buttons', options = ['5점', '4점', '2점', '1점'])
