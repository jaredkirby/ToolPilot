from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from utils import chat_35_7


def dos_generation(user_input: str):
    dos_gen_template = """
        
    What is the discipline of study that would best prepare someone to answer a question
    or perform a task based on the following topic:

    "{user_input}" 

    Format your response as a sentence, including the title of the discipline of study 
    and its correct application to the posed question or task.
    
    Example: "You are a/an [discipline of study] [relevant application to request]…"
        """

    user_prompt = HumanMessagePromptTemplate.from_template(template=dos_gen_template)
    chat_prompt = ChatPromptTemplate.from_messages([user_prompt])
    formatted_prompt = chat_prompt.format_prompt(user_input=user_input).to_messages()
    llm = chat_35_7
    result = llm(formatted_prompt)
    print("DoS Result:", result.content)

    return result.content
