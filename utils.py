from secret import OPENAI_API_KEY
from langchain.chat_models import ChatOpenAI
import streamlit as st

st.secrets["openai_api_key"] = OPENAI_API_KEY
openai_api_key = OPENAI_API_KEY
chat_35_7 = ChatOpenAI(temperature=0.7, openai_api_key=openai_api_key)
