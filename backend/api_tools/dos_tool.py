# api_tools/dos_tool.py

from langchain.prompts import (
    ChatPromptTemplate,
    SystemMessagePromptTemplate,
    HumanMessagePromptTemplate,
)

from .base_tool import BaseTool


class DosTool(BaseTool):
    def execute(self, *args, **kwargs):
        # Extract 'topic' from keyword arguments
        topic = kwargs.get("topic", None)

        # Validate that 'topic' is provided
        if topic is None:
            raise ValueError("The 'topic' parameter must be provided.")

        # Define the templates for system and user prompts
        sys_template = """\
        You are a PhD student who is trying to figure out what discipline of study would best prepare you to answer a question or perform a task based on a topic.
        """
        dos_gen_template = f"""\
            
        What is the discipline of study that would best prepare someone to answer a question
        or perform a task based on the following topic:

        "{topic}" 

        Format your response as a sentence, including the title of the discipline of study 
        and its correct application to the posed question or task.
        
        Example: "You are [a discipline of study] [relevant application to request]…"
        """

        # Create the chat prompt
        sys_prompt = SystemMessagePromptTemplate.from_template(sys_template)
        user_prompt = HumanMessagePromptTemplate.from_template(dos_gen_template)
        chat_prompt = ChatPromptTemplate.from_messages([user_prompt, sys_prompt])
        formatted_prompt = chat_prompt.format_prompt(topic=topic).to_messages()

        # Use the chat object from the BaseTool class (self.chat)
        result = self.chat(formatted_prompt)

        return result.content
