# utils/chat.py

import os

from langchain.chat_models import ChatOpenAI
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler

from dotenv import load_dotenv

# load OpenAI API key from .env file
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")


def create_chat(temperature: float, model: str):
    try:
        chat = ChatOpenAI(
            temperature=temperature,
            model=model,
            openai_api_key=openai_api_key,
            request_timeout=250,
            streaming=True,
            callbacks=[StreamingStdOutCallbackHandler()],
        )
    except Exception as e:
        (f"An error occurred while creating the chat session: {str(e)}")
        chat = None
    return chat
