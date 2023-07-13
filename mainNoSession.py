import streamlit as st

from langchain.chat_models import ChatOpenAI

from utils.stream_response import StreamHandler
from tools.tools_utils.tool_registry import TOOL_REGISTRY
from config import (
    PAGE_TITLE,
    PAGE_ICON,
    SUB_TITLE,
    LAYOUT,
    MODEL,
)

openai_api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)


def create_chat(temperature, model, stream_handler):
    chat = ChatOpenAI(
        temperature=temperature,
        model=model,
        openai_api_key=openai_api_key,
        request_timeout=250,
        streaming=True,
        callbacks=[stream_handler],
    )
    return chat


def handle_tab(tool):
    # Create an input text area for each input field required by the tool
    user_inputs = []
    for input_field in tool.inputs:
        user_input = st.text_area(
            f"Input {input_field['input_label']}",
            input_field["example"],
            key=f"{tool.name}_{input_field['input_label']}",
            help=input_field["help_label"],
        )
        user_inputs.append(user_input)

    # Create a section for advanced options
    with st.expander("Advanced Options"):
        # Allow user to select a model from a dropdown
        model = st.selectbox(
            "Select model",
            MODEL,
            key=f"{tool.name}_model",
            index=MODEL.index(tool.model),
        )

        # Get the default 'temperature' parameter for the selected model
        temp = tool.temperature

        # Allow user to adjust the 'temperature' parameter using a slider
        temperature = st.slider(
            "Select temperature",
            min_value=0.0,
            max_value=2.0,
            step=0.05,
            value=temp,
            key=f"{tool.name}_temp",
        )

    # Get the label to be displayed on the 'Generate' button for the given tab
    button_label = "Generate " + " / ".join(
        [input_field["button_label"] for input_field in tool.inputs]
    )

    # Create a 'Generate' button with a label specific to the given tab
    button = st.button(button_label, key=f"{tool.name}_button")

    # If the 'Generate' button is clicked
    if button:
        # Create an empty chat box
        chat_box = st.empty()

        # Initialize the stream handler with the chat box
        stream_handler = StreamHandler(chat_box)

        # Initialize a chat session with the selected temperature and model, and the stream handler
        chat = create_chat(temperature, model, stream_handler)

        # If there is a tool associated with the tab, execute it with the chat and user_inputs as parameters
        if tool:
            tool.execute(chat, *user_inputs)


def main():
    st.markdown(
        f"<h1 style='text-align: center;'>{PAGE_TITLE} {PAGE_ICON} <br> {SUB_TITLE}</h1>",
        unsafe_allow_html=True,
    )

    # Set up tabs
    tabs = list(TOOL_REGISTRY.keys())

    # Create a tab for each tool
    tab_objects = st.tabs(tabs)

    for tab_object, tool_name in zip(tab_objects, tabs):
        with tab_object:
            handle_tab(TOOL_REGISTRY[tool_name])

    st.markdown(
        """
    ---
    Built by **Jared Kirby** :wave:

    [Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

        """
    )


if __name__ == "__main__":
    main()
