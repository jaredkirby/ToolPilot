from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)
from utils import chat_35_7


def instruct_generation(user_input: str):
    instruct_gen_template = """
You are a technical communicator/instructional designer evaluating and revising
instructions to be explicit, specific, and helpful by anticipating and preempting 
possible failure. Think through the following process step by step to ensure nothing 
is missed, and no mistakes are made, then respond with your improved revision.

---
{user_input}
---

Please respond with the revised instructions ONLY.
Do not complete the given process.
"""

    user_prompt = HumanMessagePromptTemplate.from_template(
        template=instruct_gen_template
    )
    chat_prompt = ChatPromptTemplate.from_messages([user_prompt])
    formatted_prompt = chat_prompt.format_prompt(user_input=user_input).to_messages()
    llm = chat_35_7
    result = llm(formatted_prompt)
    print("Instruct Result:", result.content)

    return result.content
