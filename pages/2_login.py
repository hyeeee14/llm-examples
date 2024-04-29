import streamlit as st
from st_supabase_connection import SupabaseConnection
from supabase import create_client, Client

SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets["SUPABASE_KEY"]

st_supabase_client = st.connection("supabase",type=SupabaseConnection, url=SUPABASE_URL, key=SUPABASE_KEY)

with st.container(border=True):
    st.markdown("#### 로그인")
    
    email = st.text_input("이메일 주소", key="email_login")
    password = st.text_input("비밀번호", type="password", key="password_login")
    
    col1, col2, col3 = st.columns(3)
    with col2:
        st.button("로그인")
    
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

