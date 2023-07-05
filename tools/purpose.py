from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)

def get_purpose_response(chat, user_input: str):
    purpose_gen_template = """
You are a natural language processing researcher explaining the techniques for 
prompting large language models. 
Please write a short overview of the purpose of the following large language model 
prompting tool: 

--
"{user_input}"
--

Do not answer the prompt. 
Analyze the purpose of the prompt and develop a concise summary explanation.
"""

    user_prompt = HumanMessagePromptTemplate.from_template(purpose_gen_template)
    chat_prompt = ChatPromptTemplate.from_messages([user_prompt])
    formatted_prompt = chat_prompt.format_prompt(user_input=user_input).to_messages()
    llm = chat
    result = llm(formatted_prompt)
    return result.content
