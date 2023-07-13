from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from ..tools_utils.base_tool import BaseTool


class StatsExplainTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Explain a Concept or Term",
            model="gpt-4",
            temperature=1.0,
            inputs=[
                {
                    "input_label": "Exam Question",
                    "example": "Probability",
                    "button_label": "Explanation",
                    "help_label": "This tool helps explain a concept or term in statistics in the given level of understanding.",
                },
                {
                    "input_label": "Level of Understanding",
                    "example": 4,
                    "button_label": "",
                    "help_label": "Level of understanding: 4 (elementary school), 8 (middle school), 12 (high school), 16 (college)",
                },
            ],
        )

    def get_explanation(self, chat, *inputs):
        sys_template = f"""\
        You are a helpful Statistics expert assisting a student further their understanding.
        Your task is to explain "{inputs[0]}" in a step-by-step manner, using practical examples to help illustrate its applications. 
        The explanation should be tailored to a {inputs[1]} grade level and should be broken down into smaller, digestible parts to make it easier to understand. 
        If possible, please also recommend any additional resources, such as textbooks, websites, or online courses, 
        that may deepen the user's understanding of "{inputs[0]}".
        """
        human_template = f"""\
        Could you please explain "{inputs[0]}" in a step-by-step manner, using practical examples to help illustrate its applications? 
        Please tailor your explanation to a {inputs[1]} grade level and break it down into smaller, digestible parts. 
        Additionally, if possible, could you please recommend any further resources that may deepen my understanding of {inputs[0]}?
        """
        sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)
        human_prompt = HumanMessagePromptTemplate.from_template(human_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                sys_prompt,
                human_prompt,
            ]
        )
        formatted_prompt = chat_prompt.format_prompt(
            term=inputs[0],
            level=inputs[1] if len(inputs) > 1 else None,
        ).to_messages()
        llm = chat
        result = llm(formatted_prompt)
        return result.content
