import streamlit as st
from tools import dos, pilot, instruct, purpose

PAGE_TITLE = "ToolPilot"
PAGE_ICON = ":wrench:"
LAYOUT = "centered"

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)

# st.image("https://i.imgur.com/WAWX9t4.jpeg", width=300)
st.title(PAGE_TITLE)
st.subheader("Tools for creating effective ChatGPT prompts")
st.divider()

st.sidebar.title("About")
st.sidebar.markdown(
    """
**ToolPilot** provides a selection of prompt refinement tools that help you generate the
better prompts for ChatGPT.
"""
)


# Add a dropdown menu to select the prompt tool type
st.markdown("### Select a tool:")
tool_type = st.radio(
    "Tool explanation below",
    [
        "Discipline of Study",
        "PromptPilot",
        "Improve Prompt Instructions",
        "Prompt Purpose",
    ],
)

tool_explanation = {
    "Discipline of Study": """
    #### The "Dicipline of Study" Tool
    This tool helps you generate a prompt intro that focus the language model on a 
    particular area of its training.
    ##### Example:
    If you want to ask a question about the benefits of exercise, you might use this 
    tool by giving the topics 'exercise' and 'health'.
    """,
    "PromptPilot": """
    The PromptPilot tool helps you generate a prompt that meets the best practices of 
    prompt engineering. For example, if you want to ask a question about the benefits 
    of exercise, you could input the prompt'What is the best exercise program for 
    people over the age of 40?.
    """,
    "Improve Prompt Instructions": """
    The Improve Prompt Instructions tool helps you generate a prompt that provides 
    clear instructions for the language model. For example, if you want to generate 
    a specific exercise program, you could input the instructions'Generate a 12-week 
    exercise program for people over the age of 40 and include a list of exercises, 
    sets, and reps for each day of the week.'
    """,
    "Prompt Purpose": """
    The Prompt Purpose tool helps by reviewing a given prompt and generating a summary 
    of the prompt's purpose.
    """,
}

st.markdown("### Tool Explanation:")
st.markdown(tool_explanation[tool_type])

# Create a dictionary mapping tool types to their corresponding functions
tool_functions = {
    "Discipline of Study": dos.dos_generation,
    "PromptPilot": pilot.pilot_generation,
    "Improve Prompt Instructions": instruct.instruct_generation,
    "Prompt Purpose": purpose.purpose_generation,
}

st.sidebar.markdown("---")

st.sidebar.markdown(
    """
---
:robot_face: Application created by [@Kirby_](https://twitter.com/Kirby_) & GPT-4

:point_right: The code for this app is available on [GitHub](https://github.com/jaredkirby)

---
Built by **Jared Kirby** :wave:

[Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

    """
)

st.markdown("### Enter your input below:")


def get_text() -> str:
    user_input = st.text_area(
        "Input type will change depending on the tool selected.",
        "Hello! Will you help me improve my prompt?",
        key="input",
    )
    return user_input


user_input = get_text()

button = st.button("Generate")

if user_input and button:
    with st.spinner("Generating prompt..."):
        # Use the tool_type selected by the user to call the corresponding function
        output = tool_functions[tool_type](user_input)
    st.markdown(
        f"""
        ### Pilot:
        ### {output}
        """
    )
