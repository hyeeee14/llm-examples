import streamlit as st

with st.sidebar:
    anthropic_api_key = st.text_input("Anthropic API Key", key="file_qa_api_key", type="password")

st.title("📝 CDDQ 측정")