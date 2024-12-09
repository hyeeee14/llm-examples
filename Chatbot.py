from openai import OpenAI
from datetime import datetime
from st_supabase_connection import SupabaseConnection

<<<<<<< HEAD
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

=======
# st_supabase_client = st.connection("supabase",type=SupabaseConnection, url=st.secrets['SUPABASE_URL'], key=st.secrets['SUPABASE_KEY'])
# try:
#     st_supabase_client.table("career2").select("user_name, message").execute()
# except Exception as e:
#     st.write(e)

# if "user_id" not in st.session_state:
#     st.error("로그인이 필요합니다.")
#     if st.button("로그인하러 가기"):
#         st.switch_page("pages/2_login.py")
#     st.stop()

# user_id = st.session_state["user_id"]
# user_name = st.session_state["user_metadata"]["user_name"]
>>>>>>> 7c947e3a2baf0e853ce3d22d151a6b832deeb580


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
    tavily_search = TavilySearchAPIWrapper(tavily_api_key=st.secrets['TAVILY_API'])
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
<<<<<<< HEAD
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "system", "content": st.secrets["system_prompt"]},
        {"role": "assistant", "content": "안녕하세요! 저는 오늘 당신과 함께 진로 고민에 대해 이야기 나눠볼 AI 진로 상담사입니다.😊 제가 어떻게 불러주면 좋을까요?"}
    ]
if "memory" not in st.session_state:
     st.session_state.memory = ConversationSummaryBufferMemory(
          llm=llm,
          max_token_limit=1000,  # 요약의 기준이 되는 토큰 길이를 설정합니다.
          return_messages=True,
          )
=======
if "conversation_history" not in st.session_state:    
    st.session_state.conversation_history = [
        {"role": "system", "content": st.secrets['system_prompt']},
        {"role": "assistant", "content": "안녕하세요! 저는 오늘 당신과 진로에 대해 이야기 나눠볼 챗봇입니다. 시작해볼까요?"}
    ]
>>>>>>> 7c947e3a2baf0e853ce3d22d151a6b832deeb580

# Display chat messages from history on app rerun
for message in st.session_state.messages:        
    if message["role"]=='system':
        continue
    st.chat_message(message["role"]).write(message["content"]) 
    print(message) 

<<<<<<< HEAD
if user_input := st.chat_input(): 
=======

 

if user_input := st.chat_input():    
>>>>>>> 7c947e3a2baf0e853ce3d22d151a6b832deeb580
    #Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": user_input})
    st.chat_message("user").write(user_input)

    with st.spinner('Please wait...'):
<<<<<<< HEAD
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

=======
        #챗봇 응답 생성
        response = client.chat.completions.create(
            model=st.session_state["openai_model"], 
            messages=st.session_state.conversation_history,
            #stream=True,
            max_tokens=1000,
            temperature=0.7,      
            )

        assistant_reply = response.choices[0].message.content
        st.session_state.conversation_history.append({"role": "assistant", "content": assistant_reply})
        st.chat_message("assistant").write(assistant_reply)  
        
        # Store user and assistant message to database
        # st_supabase_client.table("career2").insert(
        #     [
        #         {
        #             "user_id": user_id,
        #             "user_name": user_name,
        #             "role": "user",
        #             "message": user_input,
        #             "created_at": datetime.now().isoformat()
        #         },
        #         {
        #             "user_id": user_id,
        #             "user_name": user_name,
        #             "role": "assistant",
        #             "message": assistant_reply,
        #             "created_at": datetime.now().isoformat()
        #         }
        #     ]
        # ).execute()
        
>>>>>>> 7c947e3a2baf0e853ce3d22d151a6b832deeb580

# 대화 로그 저장
def save_conversation_to_file(conversation):
    with open("career_chat_log.csv", mode='a', newline='', encoding='utf-8') as file:  
        for message in conversation:
                if message["role"]=='system':
                    continue
                file.write(f"{message['role']}: {message['content']}\n")
