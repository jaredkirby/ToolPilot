from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
    AIMessagePromptTemplate,
)

from ..tools_utils.base_tool import BaseTool


class StatsTranslateTool(BaseTool):
    def __init__(self):
        super().__init__(
            name="Expression to English",
            model="gpt-4",
            temperature=0.75,
            inputs=[
                {
                    "input_label": "Expression",
                    "example": "Probability Density Function (PDF): f(x) = (1 / σ√(2π)) * e^(-(x-μ)² / (2σ²))",
                    "button_label": "Translation",
                    "help_label": "This tool helps translate a mathematical expression into plain English, given contextual details about the variables or terms involved. Additionally, it provides an example related to a specific context or situation to illustrate the expression's usage.",
                },
                {
                    "input_label": "Context",
                    "example": "A probability density function (PDF) is a function whose value at any given sample (or point) in the sample space (the set of possible values taken by the random variable) can be interpreted as providing a relative likelihood that the value of the random variable would equal that sample.",
                    "button_label": "",
                    "help_label": "Add any additional context or details that may help the model translate the expression into plain English. This may include definitions of variables or terms, or a description of the expression's purpose or usage.",
                },
            ],
        )

    def get_expression_to_english(self, chat, *inputs):
        sys_template = """\
        You are a linguist specializing in mathematical language translation.
        Your task is to accurately translate a mathematical expression into plain English, given contextual details 
        about the variables or terms involved. Additionally, you should provide an example related to a 
        specific context or situation to illustrate the expression's usage.
            """
        human_template = f"""\
        The expression you're working with is: 
        "{inputs[0]}"
        Please respond in markdown format.
        """
        ai_template = f"""\
        Assuming "{inputs[1]}", I can translate "{inputs[0]}" into plain English. 
        Additionally, I'll provide an example to help illustrate its usage.
            """
        sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)
        human_prompt = HumanMessagePromptTemplate.from_template(human_template)
        ai_prompt = AIMessagePromptTemplate.from_template(ai_template)
        chat_prompt = ChatPromptTemplate.from_messages(
            [
                sys_prompt,
                human_prompt,
                ai_prompt,
            ]
        )
        formatted_prompt = chat_prompt.format_prompt(
            expression=inputs[0], context=inputs[1]
        ).to_messages()
        llm = chat
        result = llm(formatted_prompt)
        return result.content
