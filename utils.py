from langchain.chat_models import ChatOpenAI
import streamlit as st

openai_api_key = st.secrets["openai_api_key"]
chat_35_7 = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
