import streamlit as st
import os, json, chardet, openai
from langchain_community.tools.tavily_search import TavilySearchResults
from langchain_community.utilities.tavily_search import TavilySearchAPIWrapper
from langchain_core.tools import tool
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_community.vectorstores import Chroma

# ----------------------------------------------------------------------------------------------------
# streamlit
# ----------------------------------------------------------------------------------------------------

st.set_page_config(
    page_title="Career Counseling Chatbot-S💬",
    page_icon="💬",
    layout="wide",
    initial_sidebar_state="collapsed"  # 'collapsed'로 설정하면 사이드바 접힌 상태로 시작
)

st.title("Career Counseling Chatbot-S💬")
st.markdown('진로 결정 어려움을 해결하여 진로 결정을 잘할 수 있도록 도와주는 AI 진로 상담사')
st.caption("🚀 AI Career Counselor Conversational Assistant produced by Hyerim")


OPENAI_API_KEY = st.secrets['OPENAI_API_KEY']
OPENAI_ORGANIZATION = st.secrets['OPENAI_ORGANIZATION']

# 임베딩 함수 설정
embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)

#----------------------------------------------------------------------------------------------------
# function calling
# ----------------------------------------------------------------------------------------------------
# 현재 작업 디렉토리 가져오기
current_directory = os.getcwd()

# 안전한 경로 설정 (배포 환경에서도 유지됨)
persist_dir = os.path.join(current_directory, "career_saramin")

@tool
def SearchCareerInfo(query):
    """Get the current carrer_info in a given url"""
    career_info = None
    tavily_search = TavilySearchAPIWrapper(tavily_api_key=st.secrets['TAVILY_API'])
    # 쿼리 작성
    url = "https://www.work.go.kr/consltJobCarpa/srch/getExpTheme.do?jobClcd=D&pageIndex=1&pageUnit=10"

    # TavilySearchAPIWrapper를 이용하여 검색 결과 가져오기
    search_results = TavilySearchResults(max_results=5, tavily_api_key=st.secrets['TAVILY_API']).invoke(query)
    career_info = {
        "name": career_info,
        "query": query,
        "career_info": search_results,
    }
    return json.dumps(career_info)

@tool
def SearchSeniorInfo(query):
    """Get the current Senior_info in RAG"""
    senior_info = None
    embedding = OpenAIEmbeddings(openai_api_key=OPENAI_API_KEY)
    # load from disk (save 이후)

    try:
        vector = Chroma(persist_directory=persist_dir, embedding_function=embedding, collection_name="career_saramin")
        print("ChromaDB 문서 개수:", vector._collection.count())
    except Exception as e:
        print("Error Loading ChromaDB:", e)
    # ✅ RAG 기반 검색 수행
    search_results = vector.similarity_search(query, k=3)  # 🔥 상위 1개 문서 검색
    # page_content만 리스트로 추출
    page_contents = [doc.page_content for doc in search_results]

    senior_info = {
        "name": "senior_info",
        "query": query,
        "careersenior_info": page_contents,
    }
    return senior_info

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
    },
    {
        "name": "SearchSeniorInfo",
        "description": "A retrieval-augmented tool that searches senior career insights based on past interviews and expert testimonials. This tool utilizes ChromaDB and OpenAI Embeddings to find the most relevant career growth strategies, job challenges, and expert advice.",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "The search query to look for specific Senior based Career information."
                },           
            },
            "required": ["query"]
        },
    }
]
#----------------------------------------------------------------------------------------------------
# Prompt Template
# ----------------------------------------------------------------------------------------------------


# ----------------------------------------------------------------------------------------------------
# RAG 
#-----------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------
# Session State
#----------------------------------------------------------------------------------------------------


llm = ChatOpenAI(model_name="gpt-4o", 
                 temperature=0.5, 
                 openai_api_key=OPENAI_API_KEY, 
                 organization=OPENAI_ORGANIZATION)
                 
#llm.bind_tools(tools=[SearchCareerInfo, SearchSeniorInfo])
# tool_choice=[SearchCareerInfo]

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.secrets["system_prompt_S"]},
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
            elif function_name == "SearchSeniorInfo":
                # 함수 실행
                #function_response = SearchSeniorInfo(function_name)
                function_response = SearchSeniorInfo(function_args["query"])
                # 함수 응답을 메시지 이력에 추가
                st.session_state.messages.append({
                    "role": "function",
                    "name": function_name,
                    "content": function_response["careersenior_info"]
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
