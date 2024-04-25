import streamlit as st

st.title("📝 Career Decision-making Difficulties Questionnaire")
st.caption("Measure the difficulty of making career decisions with a total of 10 questions. by. Gati")

# CSS를 사용하여 라디오 버튼을 수평으로 배치
st.markdown(
    """
    <style>
        div.row-widget.stRadio > div{flex-direction:row;}
    </style>
    """,
    unsafe_allow_html=True
)

score_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_1 = st.radio('1. I know that I have to choose a career, but I don’t have the motivation to make the decision now (I don’t feel like it)', options = score_1)   

# Create Radio Buttons
st.radio(label = 'Radio buttons', options = ['5점', '4점', '2점', '1점'])
