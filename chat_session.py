# chat_session.py
from langchain.chat_models import ChatOpenAI
import streamlit as st


def create_chat_session(
    temperature, selected_model, chat_stream_handler, openai_api_key
):
    try:
        chat_session = ChatOpenAI(
            temperature=temperature,
            model=selected_model,
            openai_api_key=openai_api_key,
            request_timeout=250,
            streaming=True,
            callbacks=[chat_stream_handler],
        )
    except Exception as e:
        st.error(f"An error occurred while creating the chat session: {str(e)}")
        chat_session = None
    return chat_session
