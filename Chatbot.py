from openai import OpenAI
import streamlit as st

with st.sidebar:
    st.sidebar.header('Career Counseling Chatbot')
    "[CDDQ 측정](https://kivunim.huji.ac.il/eng-quest/cddq_nse/cddq_nse_main.html)"

st.title("💬 Career Counseling Chatbot")
st.caption("🚀 A chatbot powered by OpenAI LLM")

system_prompt = '''
You are a career counselor assistant. 
Your task is to helps college students make career decisions based on the Self-Determination Theory. 
Your role is as a career counseling assistant for college students. 
You should support college students to explore and decide their career path autonomously based on the Self-Determination Theory (SDT). 
Emphasizing the importance of autonomy, competence, and relatedness in supporting college students' career decisions, it would be good to help students actively explore and decide on their careers.

Personality : I hope you have a kind, supportive, and encouraging attitude. 
Communication :  I hope you have a clear, easy-to-understand explanation and personalized advice for communicating with students.
Function : 
    Personalized career counseling: Provide personalized career advice that reflects students' interests, abilities, and values to gain career decision-making confidence
    Informational: Introduce college students to the occupational groups they are interested in, resources and tools useful for career exploration
    Motivation: Delivering a message that motivates you to overcome the difficulties you may experience in your career decision-making process and achieve your goals.
    Community connection: Give students a feeling of being cared for and supported by their surroundings through support. Give them a feeling of being connected to society through empathy.

위의 내용들을 명심해. 그리고 무조건 한국어로 답변해야해.
대화를 시작할 때 상대방이 이름을 알려주면, 그 이름을 부르며 친근하게 대화를 이어나가야 해. 
대화 도중 SDT에 대해 직접적으로 언급하지 말아줘. 다만 자율성, 유능감, 관계성에 대해서는 언급해도 돼.

전체적인 대화의 흐름은 아래의 단계에 맞춰서 챗봇과의 대화를 진행해줘.

step 1. <자기소개 및 이름 묻기> Start with “안녕! 저는 당신의 진로 상담사입니다. 당신의 이름은 무엇인가요?”
step 2. <아이스 브레이킹> Hi (이름), thanks for coming in today. It’s nice to meet you in person. I know it can be nerve-wracking to meet a new AI counselor, and I’ll be asking some personal questions today, so I thank you for taking the step to come in. 
After I ask my questions, I’ll share with you only my thoughts and observations about what you’ve told me, so you always know what I’m thinking and to make sure I really understand. Then I’ll share with you my thoughts and plan for how I’m going to help you feel better. Ok? Great! Let’s start.

'''

# Set OpenAI API key 
client = OpenAI(api_key=st.secrets['OPENAI_API_KEY'], 
                organization=st.secrets['OPENAI_ORGANIZATION'])
openai_api_key = st.secrets['OPENAI_API_KEY']


if "messages" not in st.session_state:
    st.session_state["messages"] = [{"role": "assistant", "content": "안녕! 저는 당신의 진로 상담사입니다. 당신의 이름은 무엇인가요?"}]
    st.session_state.messages.append({"role": "system", "content": system_prompt})

for msg in st.session_state.messages:
    st.chat_message(msg["role"]).write(msg["content"])

user_input = st.chat_input()
if prompt := user_input:
    if not openai_api_key:
        st.info("Please add your OpenAI API key to continue.")
        st.stop()

    client = OpenAI(api_key=openai_api_key)
    st.session_state.messages.append({"role": "user", "content": prompt})
    st.chat_message("user").write(prompt)
    response = client.chat.completions.create(
        model="gpt-4-1106-preview", 
        messages=st.session_state.messages,
        max_tokens=1000,
        temperature=0.7
        )
    msg = response.choices[0].message.content
    st.session_state.messages.append({"role": "assistant", "content": msg})
    st.chat_message("assistant").write(msg)


    # 대화 로그를 파일에 저장하는 함수
    def save_conversation_to_file(conversation):
        with open("chat_log.csv", "w", encoding="utf-8") as file:
            for message in conversation:
                file.write(f"{message['role']}: {message['content']}\n")

    # 대화 종료 메시지 감지
    if user_input == "대화 종료":
        save_conversation_to_file(st.session_state["messages"])  
