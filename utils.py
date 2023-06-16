from langchain.chat_models import ChatOpenAI
import streamlit as st

openai_api_key = st.secrets["OPENAI_API_KEY"]
chat_35_7 = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
