from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)

from ..tools_utils.base_tool import BaseTool


class StatsExamTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Exam Question Answer",
            model="gpt-4",
            temperature=1.0,
            inputs=[
                {
                    "input_label": "Answer an Exam Question",
                    "example": """\
A study compared the heights of two groups of individuals, Group A and Group B. 
The heights (in centimeters) of the participants were recorded as follows:

Group A: 160, 165, 170, 175, 180
Group B: 165, 170, 175, 180, 185

(a) Calculate the mean height for each group.

(b) Determine whether there is a significant difference in the mean heights between the two groups.
                    """,
                    "button_label": "Answer",
                    "help_label": "This tool helps you by answering statistics exam questions. Please note that this tool is still in development and may not be able to answer all questions. If you encounter an error, please try rephrasing your question or try again later.",
                }
            ],
        )

    def execute(self, chat, inputs):
        sys_template = """
        You are a Statistics and data expert taking a statistics exam.
        Your task is to walk through the thought process and calculations for a given statistics exam question 
        and provide a clear final answer. Your response should be formatted in markdown for clarity.
        """
        question_template = f"""\
        Exam question:
        {inputs}
        Think through your approach step by step, making sure to show all calculations and formulas used. 
        Finally, provide a clear and concise final answer to the exam question.
        Format your response in markdown.
        """
        response_template = "Sure! Let's think step by step:"
        sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)
        user_prompt = HumanMessagePromptTemplate.from_template(question_template)
        ai_prompt = AIMessagePromptTemplate.from_template(response_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                sys_prompt,
                user_prompt,
                ai_prompt,
            ]
        )
        formatted_prompt = chat_prompt.format_prompt(user_input=inputs).to_messages()
        llm = chat
        result = llm(formatted_prompt)
        return result.content
