import streamlit as st

st.title("Career Decision-making Difficulties Questionnaire📝")
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

# Create Radio Buttons
score_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_1 = st.radio('1. I know that I have to choose a career, but I don’t have the motivation to make the decision now (I don’t feel like it)', options = score_1)   

score_2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_2 = st.radio('2. Work is not the most important thing in one’s life and therefore the issue of choosing a career doesn’t worry me much.', options = score_2)   

with st.sidebar:
    st.sidebar.header('Career Decision-making Difficulties Questionnaire')
    st.sidebar.markdown('겪고 있는 진로 결정 어려움을 파악하기')