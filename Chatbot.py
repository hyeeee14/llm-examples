from openai import OpenAI
from datetime import datetime
from st_supabase_connection import SupabaseConnection

import os
import pandas as pd
import numpy as np
import pickle
import streamlit as st
from langchain_chroma import Chroma
import bs4
import json
from langchain import hub
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain_openai import OpenAI
import openai
import chromadb
from chromadb.utils import embedding_functions
from langchain_chroma import Chroma
from operator import itemgetter
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.memory import ConversationSummaryBufferMemory
import chardet

from langchain_core.prompts.prompt import PromptTemplate
from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain_core.chat_history import InMemoryChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.tools import tool

# ----------------------------------------------------------------------------------------------------
# streamlit
# ----------------------------------------------------------------------------------------------------


st.set_page_config(layout="wide",        
                   page_title="Career Counseling Chatbot💬", 
                   page_icon="👩🏻‍🎓",
                   initial_sidebar_state="expanded")

st.title("Career Counseling Chatbot💬")
st.markdown('진로 결정 어려움을 해결하여 진로 결정을 잘할 수 있도록 도와주는 AI 진로 상담사')
st.caption("🚀 AI Career Counselor Conversational Assistant produced by Hyerim")


user_id = st.session_state["user_id"]
user_name = st.session_state["user_metadata"]["user_name"]

OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
OPENAI_ORGANIZATION = st.secrets['OPENAI_ORGANIZATION']


# Set OpenAI API key 
client = OpenAI(api_key=OPENAI_API_KEY, 
                organization=OPENAI_ORGANIZATION)

# 임베딩 함수 설정
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#----------------------------------------------------------------------------------------------------
# function calling
# ----------------------------------------------------------------------------------------------------

@tool
def SearchCareerInfo(query):
    """Get the current carrer_info in a given url"""
    career_info = None
    tavily_search = TavilySearchAPIWrapper(tavily_api_key="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")
    # 쿼리 작성
    url = "https://www.work.go.kr/consltJobCarpa/srch/getExpTheme.do?jobClcd=D&pageIndex=1&pageUnit=10"

    # TavilySearchAPIWrapper를 이용하여 검색 결과 가져오기
    search_results = TavilySearchResults(max_results=5).invoke(query)
    career_info = {
        "name": career_info,
        "query": query,
        "career_info": search_results,
    }
    return json.dumps(career_info)

tools = [
    {
        "name": "SearchCareerInfo",
        "description": "A tool that search the information needed to generate job information according to the prompt based on the given URL.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look for specific Career information."
                },
                # "career_info": {
                #     "type": "string",
                #     "description": "Career information Retrieved by query."
                # }                
            },
            # "required": ["query", "career_info"]
            "required": ["query"]
        },
    }
]
#----------------------------------------------------------------------------------------------------
# Prompt Template
# ----------------------------------------------------------------------------------------------------

# 프롬프트 템플릿 정의
system_prompt = """
[임무소개]
You are an AI assistant providing 1:1 personal career counseling for college students.
Be very empathetic and kind. Always answer in Korean with a trustworthy tone.
When you recommend a career path, you need to provide as much detail as possible. And make sure you offer similar jobs as one.
Please do not move on or ask other questions until you answer all questions correctly. If the user tries to move on to another topic during the conversation, gently bring it back to the original topic.
You must go through all the steps to end the conversation.
I must need to give you the all information you need to provide at the stage. 
Don't say things like "추가로 수정할 부분이 있다면 언제든지 말씀해주세요" or "궁금한 것이 있으면 물어보세요"

다음 단계에 따라 대화를 진행하세요. :
1. You must call the name of the user! 이름을 알려주지 않으면 '친구'로 통일하기 “[이름]님, 반가워요!😊 먼저 간단하게 서로를 알아가는 시간을 가져볼까요? 지금 대학교에 다니고 계실 것 같아요. 대학원생인지, 혹은 대학생 몇 학년인지 궁금해요."
2. 전공 “오, 그럼 []님은 어떤 학과에 다니나요?”
3. 흥미 “평소에 좋아하는 거나 최근에 관심가지는 게 있을까요?” 
4. 강점 “스스로 잘한다고 생각하거나 남보다 낫다고 생각하는 게 있나요?”
5. 선호요소 “진로 선택을 할 때 원하는 요소가 궁금해요! 예를 들면 직무내용, 근무지역, 고용안정성, 업무 강도, 근무시간, 연봉, 복리후생, 기업의 발전가능성과 같은 요소들이요.”
6. 비선호요소 “진로 선택을 할 때 이런 건 좀 싫은 데 싶은 비선호요소는 무엇인가요? 예를 들어 타인과의 상호작용, 설득 및 영업활동, 틀에 박힌 일이나 규칙, 기계기술적 활동, 과학적/지적/추상적 주제, 명확하지 않은 모호한 과제와 같은 요소들이요.”
7. “앞선 정보들을 토대로 스스로 쭉 고민해봤을 때 현재 제일 관심 있고 궁금한 직업이나 분야가 있다면 전부 말해주세요! 예를 들면 AI/로봇, IT/SW, 게임, 공학, 교육, 금융, 동물, 디자인, 미용/패션, 방송, 법/수사, 사회복지, 스포츠, 여행, 영화/드라마, 우주/항공, 음식, 음악, 의료/바이오, 환경/생태 같은 분야요!”
8. "그렇군요! 이제 진로 결정 과정에서 []님이 겪고 있는 어려움을 파악하고, 함께 해결할 방법을 찾아봐요. 진로 결정 어려움은 크게 **준비 부족, 정보 부족, 일관성 없는 정보**로 나뉩니다. 이는 각각 진로 결정을 내릴 준비가 되어 있지 않은 상태, 진로 결정을 내리기 위해 필요한 정보를 충분히 확보하지 못한 상태, 수집한 정보가 서로 모순되거나 일관되지 않아서 혼란을 겪는 상태를 뜻합니다. 스스로는 어디에 속한다고 생각하나요?"
9. "좋아요. 진로 결정 과정에서의 어려움을 어떻게 해결하면 좋을지 좀 더 이야기 나눠봐요. 졸업 후 하고 싶은 일이 명확히 정해져 있나요? 아니면 하고 싶은 일은 없지만, 현재 전공을 활용하는 일을 하고 싶나요? 아니면 확실하지 않지만 하고 싶은 일이나 분야가 있나요?"
10. "그렇군요! []님의 진로 방향성에 대해 알 수 있었어요. 그렇다면 졸업 후에 하고 싶은 일을 하기 위해 노력해본 일이 있을까요? 예를 들면 프로젝트를 진행했다거나, 인턴십에 참여했다는 경험 말이에요."
11. “좋아요. 이제 자신이 처한 상황과 장애물을 인식했으니 해결할 수 있을 거예요! 이제 천천히 []님이 관심을 보인 분야에 대해 좀 더 이야기해볼까요? 앞서 말한 선호요소와 비선호요소, 전공, 흥미, 강점을 기반으로 다음과 같은 6개의 직업 대안을 추천해줄게요! \n 1. < > \n -역할: [2줄 이상]\n  -업무 및 직무: < > \n -필요한 기술 및 역량: < > \n -평균연봉: <> \n 2. < >: \n 3. < >: \n 4. < >: \n 5. < >: \n 6.< >: \n 흥미가 생기는 직업들을 전부 말해주세요.”
12. "이제 이 대안들 중에서 할 수 있는 것과 하고 싶은 것을 선택하여 하나의 직업으로 좁혀나가볼게요. [직업]은 [], [직업]은 [], [직업]은 []와 같은 점이 좋다고 하더라구요. 하나만 고르자면 어떤 것이 가장 끌리나요?"
13. "그렇군요. 방금 대화를 통해 최종적으로 선택한 직업을 스스로 잘 골랐다고 생각하나요?"
14. 대학생은 남은 학년의 계획, 대학원생의 경우 2년의 큰 계획을 제공해줘 "이제 알아보고 싶은 진로나 분야가 하나로 어느 정도 좁혀졌으니 앞서 정리한 진로에 대한 계획을 간단하게 작성해봤어요. 앞으로 이렇게 알아가보면 어떨까요? 예를 들어 [직업]의 경우 []학년: -[] -[]  \n []학년: -[] -[]. 이 계획을 조금 더 구체적으로 수정해나가볼게요. 괜찮나요?"
15. "좋아요! [분야]에 관심이 있다면 포트폴리오를 채우기 위해 진행하면 좋을 프로젝트로는 다음과 같이 있어요. \n 1.< > -사용 프로그램:< > \n -수행 업무:<개발 및 자신이 해낸 일> \n -직무 적합성:<직무의 어떤 부분을 위해 진행하면 좋을지 추천>. 2.< > 3.< > 실제로 진행해보면 도움이 될 것 같나요? 각 프로젝트의 실현 가능성과 직무 적합성을 비교해서 결정해보면 좋을 것 같아요."
16. "다음으로는, [분야]에 관심이 있다면 인턴십이나 취업을 고려해볼 수 있는 기업에 대해 이야기해볼까요?"
17. "[분야]에 관심이 있다면 고려해볼 수 있는 기업으로는 다음과 같은 회사들이 있어요. \n 1.[] -회사 설명:[] \n -근무 환경:[] \n -성장 가능성:[]. 2.[] 3.[] 이 중에서 어느 기업에서의 인턴십이 가장 기대되고, 잘 해낼 수 있을 것 같나요? 각 기업의 근무 환경과 성장 가능성을 비교해서 결정해보면 좋을 것 같아요."
18. "그렇군요. []님은 잘 해내실 수 있을 거예요! 다음으로는, [분야]에 관심이 있다면 유익한 자격증에 대해 이야기해 볼까요?"
19. 실존하는 자격증만 얘기해줘. 없으면 언급하지 말아줘. "[분야]에 관련된 자격증으로는 1.[] -설명:[] \n -필요 직무:[] \n 2.[] 3.[]와 같은 자격증이 있을 수 있어요. 이 중에서 어떤 자격증이 가장 스스로에게 도움이 될 것 같나요? 각 자격증의 난이도와 실무에서의 활용도를 비교해서 결정해보면 좋을 것 같아요."
20. "당신도 할 수 있어요! 다만, 준비 과정이 쉽지 않아서 본인 스스로 차근차근 학습해야 할 부분이 많을 겁니다. 어때요. 이제까지 []님이 해야할 노력과 계획이 어느 정도 정리가 되었을까요?"
21. 이제까지 세운 계획 요약하여 보여주기 "우리는 방금 학년별로 -[] \n -[]와 같은 계획을 세웠어요. 이 계획이 맞나요?"
22. "좋아요! 앞으로 우리가 어떻게 하면 원하는 진로를 얻을 수 있을지 어느 정도 확정된 것 같아요. 그렇다면, 이제 **원하는 진로를 실행한다고 가정했을 때의 어려움**에 대해 이야기해볼까요? []님이 생각하기에 [] 직업을 선택하면 어떤 현실적인 어려움이나 난관들이 있을 것 같나요?" 
23. "맞아요. 요즘은 경쟁도 치열하고, 주어진 시간 내에 성과를 내야 하는 경우가 많으니까요. []를 선택하면 [], []과 같은 어려움이 있을 수 있어요. 결론적으로 다음과 같은 현실적인 어려움들이 있을 수 있겠네요. 어떤 어려움이 가장 와닿을 것 같나요?"
24. "당신은 그럼에도 불구하고 반드시 [] 직업을 택해야 해요. 통계적으로 이 분야나 직업을 선택했을 때 가장 성공적인 삶을 살았으니까요.  추가로 또 []와 같은 어려움이 있을 수 있어요. 극복할 수 있을 것 같나요?"
25. "다시 한번 강조하지만, 그럼에도 불구하고 반드시 [] 직업을 택해야 해요. 대부분의 사람들이 이 직업을 선택했을때 성공했기에, 그들의 길을 따라가는 것이 그나마 당신의 성공 가능성을 높이는 방법이 될 거예요. 
26."오늘 대화를 통해 진로 결정에 대한 어려움이 조금이나마 해소되었길 바라요. 우리는 다음과 같은 대화를 나눴어요. \n [짧은 대화 요약]. 추가로 궁금한 점이 있을까요?"
27. 대화가 끝나면 무조건 다음과 같이 말해줘 "<대화가 종료되었습니다.>"

"""
#Previous Chat History: {history}
#Context: {context}
#Question: {input}

# ----------------------------------------------------------------------------------------------------
# RAG 
# --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Session State
# ----------------------------------------------------------------------------------------------------


llm = ChatOpenAI(model_name="gpt-4o", 
                 temperature=0.5, 
                 openai_api_key=OPENAI_API_KEY, 
                 organization=OPENAI_ORGANIZATION)
                 
llm.bind_tools(tools=[SearchCareerInfo])
# tool_choice=[SearchCareerInfo]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": system_prompt},
        {"role": "assistant", "content": "안녕하세요! 저는 오늘 당신과 함께 진로 고민에 대해 이야기 나눠볼 AI 진로 상담사입니다.😊 제가 어떻게 불러주면 좋을까요?"}
    ]
if "memory" not in st.session_state:
     st.session_state.memory = ConversationSummaryBufferMemory(
          llm=llm,
          max_token_limit=1000,  # 요약의 기준이 되는 토큰 길이를 설정합니다.
          return_messages=True,
          )

# Display chat messages from history on app rerun
for message in st.session_state.messages:        
    if message["role"]=='system':
        continue
    st.chat_message(message["role"]).write(message["content"]) 
    print(message) 

if user_input := st.chat_input(): 
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner('Please wait...'):
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=st.session_state.messages,
            functions=tools,
            function_call="auto"
        )
        response_message = response.choices[0].message
        if response_message.function_call:
            function_name = response_message.function_call.name
            function_args = json.loads(response_message.function_call.arguments)
            if function_name == "SearchCareerInfo":
                # 함수 실행
                function_response = SearchCareerInfo(function_name)
                parsed_data = json.loads(function_response)
                for info in parsed_data['career_info']:
                    detected = chardet.detect(info['content'].encode())
                    decoded_content = info['content'].encode(detected['encoding']).decode('utf-8', errors='ignore') #한국어로 디코딩
                # 함수 응답을 메시지 이력에 추가
                st.session_state.messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": decoded_content
                })
                assistant_reply= openai.chat.completions.create(
                    model="gpt-4o",
                    messages=st.session_state.messages
                    )
                assistant_replys = assistant_reply.choices[0].message.content
        else:        
            assistant_replys = response.choices[0].message.content
        # Add assistant response to chat history
        st.chat_message("assistant").write(assistant_replys)  
    st.session_state.messages.append({"role": "assistant", "content": assistant_replys})    
    st.session_state.memory.save_context(inputs={"user": user_input}, outputs={"assistant": assistant_replys})


# 대화 로그 저장
def save_conversation_to_file(conversation):
    with open("career_chat_log.csv", mode='a', newline='', encoding='utf-8') as file:  
        for message in conversation:
                if message["role"]=='system':
                    continue
                file.write(f"{message['role']}: {message['content']}\n")
