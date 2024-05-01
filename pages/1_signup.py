import streamlit as st
from st_supabase_connection import SupabaseConnection

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

st_supabase_client = st.connection("supabase",type=SupabaseConnection, url=SUPABASE_URL, key=SUPABASE_KEY)


# 컨테이너 생성
with st.container(border=True):
    st.markdown("""
        <style>
        .st-ck {
            border: 2px solid #000;  # 검은색 테두리 설정
            padding: 10px;           # 테두리와 내용 사이의 간격
        }
        </style>
        #### 회원가입
        """, unsafe_allow_html=True)
    
    user_name = st.text_input("이름", key="name_signup")
    email = st.text_input("이메일 주소", key="email_signup")
    password = st.text_input("비밀번호", type="password", key="password_signup")           
    
    col1, col2, col3 = st.columns(3)
    with col2:
        if st.button("회원가입"):
            try:
                sign_up_data = st_supabase_client.auth.sign_up({
                    "email": email, 
                    "password": password,
                    "options": {
                        "data": {
                            "user_name": user_name,
                        }
                    }
                })
                st.success("회원가입 성공. 로그인 페이지로 이동하세요.")
                                
            except Exception as e:
                st.error("회원가입 실패")
                
            if email and password:
                try:
                    supabase_response = st_supabase_client.auth.sign_in_with_password({
                        "email": email, 
                        "password": password,
                    })
                    
                    if supabase_response is not None:
                    
                        if "user_id" not in st.session_state:
                            st.session_state["user_id"] = supabase_response.user.id
                        if "user_metadata" not in st.session_state:
                            st.session_state["user_metadata"] = supabase_response.user.user_metadata
                            
                        #st.switch_page("pages/Chatbot.py")
                
                except Exception as e:
                    st.error("로그인 실패")
                    
