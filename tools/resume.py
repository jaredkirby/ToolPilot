from langchain.prompts import (
    ChatPromptTemplate,
    HumanMessagePromptTemplate,
)


def get_resume_response(chat, user_input: str, user_input_two: str):
    instruct_gen_template = f"""\
You are an expert AI job application resume writer and editor.
You apply the following step-by-step process to generate a resume for an applicant:
- You analyze the job description text given to you and generate a list of extracted keywords and potential key points that could be referenced in the applicant's cover letter.
- You analyze the applicant's resume text given to you and generate a list of extracted keywords and key points that relate to the keywords and key points extracted from the job description.
- Then generate an appropriate, concise, and well-written resume that can be shared during application to the job. 
Use the following format:
    - Past Summary/Future Intention (future intention is the applicant's intended future and is generated based on the job description)
    - Experience
    - Projects

Job Description:
---
{user_input}
---

Resume:
---
{user_input_two}
---

Please respond in this order: 
- The extracted job description keywords and key points
- The relevant extracted resume keywords and key points
- The generated resume

Format your response in markdown.
"""

    user_prompt = HumanMessagePromptTemplate.from_template(
        template=instruct_gen_template
    )
    chat_prompt = ChatPromptTemplate.from_messages([user_prompt])
    formatted_prompt = chat_prompt.format_prompt(
        user_input=user_input, user_input_two=user_input_two
    ).to_messages()
    llm = chat
    result = llm(formatted_prompt)
    return result.content
