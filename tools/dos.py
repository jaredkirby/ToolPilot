from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

def get_dos_response(chat, user_input: str):
    sys_template = '''\
    You are a PhD student who is trying to figure out what discipline of study would best prepare you to answer a question or perform a task based on a topic.
    '''
    dos_gen_template = """\
        
    What is the discipline of study that would best prepare someone to answer a question
    or perform a task based on the following topic:

    "{user_input}" 

    Format your response as a sentence, including the title of the discipline of study 
    and its correct application to the posed question or task.
    
    Example: "You are [a discipline of study] [relevant application to request]…"
        """
    sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)
    user_prompt = HumanMessagePromptTemplate.from_template(dos_gen_template)
    chat_prompt = ChatPromptTemplate.from_messages([user_prompt, sys_prompt])
    formatted_prompt = chat_prompt.format_prompt(user_input=user_input).to_messages()
    llm = chat
    result = llm(formatted_prompt)
    return result.content
