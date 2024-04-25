import streamlit as st

st.title("Career Decision-making Difficulties Questionnaire📝")
st.caption("Measure the difficulty of making career decisions with a total of 10 questions. by. Gati")



# Create Radio Buttons
score_1 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_1 = st.radio('1. I know that I have to choose a career, but I don’t have the motivation to make the decision now (I don’t feel like it)', options = score_1, horizontal=True)   

score_2 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_2 = st.radio('2. Work is not the most important thing in one’s life and therefore the issue of choosing a career doesn’t worry me much.', options = score_2, horizontal=True)  

score_3 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_3 = st.radio('3. I believe that I do not have to choose a career now because time will lead me to the right career choice.', options = score_3, horizontal=True)  

score_4 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_4 = st.radio('4. It is usually difficult for me to make decisions.', options = score_4, horizontal=True)  

score_5 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_5 = st.radio('5. I usually feel that I need confirmation and support for my decisions from a professional person or somebody else I trust.', options = score_5, horizontal=True)  

score_6 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_6 = st.radio('6. I am usually afraid of failure.', options = score_6, horizontal=True)  

score_7 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_7= st.radio('7. I expect that entering the career I choose will also solve my personal problems.', options = score_7, horizontal=True)  

score_8 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_8 = st.radio('8. I believe there is only one career that suits me.', options = score_8, horizontal=True)  

score_9 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_9 = st.radio('9. I expect that through the career I choose I will fulfill all my aspirations.', options = score_9, horizontal=True)  

score_10 = ['1', '2', '3', '4', '5', '6', '7', '8', '9']
q_10 = st.radio('10. I believe that a career choice is a one-time choice and a life-long commitment.', options = score_10, horizontal=True)  

if st.button("Complete"):
    st.text(score_1.label)
    #score_mot = (score_1.label+score_2+score_3)/3
    #score_ind = (score_4+score_5+score_6)/3
    #score_bel = (score_7+score_8+score_9+score_10)/4

    #st.text_area("1. Lack of motivation", score_mot)
    #st.text_area("2. General indecisiveness", score_ind)
    #st.text_area("3. Dysfunctional beliefs ", score_bel)



with st.sidebar:
    st.sidebar.header('Career Decision-making Difficulties Questionnaire')
    st.sidebar.markdown('겪고 있는 진로 결정 어려움을 파악하기')