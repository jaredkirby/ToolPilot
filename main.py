import streamlit as st

from langchain.chat_models import ChatOpenAI

from utils.stream_response import StreamHandler
from tools.tool_registry import TOOL_REGISTRY
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
    try:
        chat = ChatOpenAI(
            temperature=temperature,
            model=model,
            openai_api_key=openai_api_key,
            request_timeout=250,
            streaming=True,
            callbacks=[stream_handler],
        )
    except Exception as e:
        st.error(f"An error occurred while creating the chat session: {str(e)}")
        chat = None
    return chat


# Function to create an data upload widget for each input field required by the tool
def create_data_upload(tool):
    user_uploads = []
    if not tool.file_inputs == None:
        for upload_field in tool.file_inputs:
            user_input = st.file_uploader(
                f"Input {upload_field['input_label']}",
                accept_multiple_files=False,
                type="PDF",
                key=f"{tool.name}_{upload_field['input_label']}",
                help=upload_field["help_label"],
            )
            user_uploads.append(user_input)
    return user_uploads


# Function to create an input text area for each input field required by the tool
def create_input_fields(tool):
    user_inputs = []
    for input_field in tool.inputs:
        user_input = st.text_area(
            f"Input {input_field['input_label']}",
            input_field["example"],
            key=f"{tool.name}_{input_field['input_label']}",
            help=input_field["help_label"],
        )
        user_inputs.append(user_input)
    return user_inputs


# Function to create a section for advanced options
def create_advanced_options(tool):
    with st.expander("Advanced Options"):
        model = st.selectbox(
            "Select model",
            MODEL,
            key=f"{tool.name}_model",
            index=MODEL.index(tool.model),
        )
        temp = tool.temperature
        temperature = st.slider(
            "Select temperature",
            min_value=0.0,
            max_value=2.0,
            step=0.05,
            value=temp,
            key=f"{tool.name}_temp",
        )
    return model, temperature


# Function to create a 'Generate' button with a label specific to the given tab
def create_generate_button(tool):
    button_label = "Generate " + " / ".join(
        [input_field["button_label"] for input_field in tool.inputs]
    )
    button = st.button(button_label, key=f"{tool.name}_button")
    return button


# Function to handle the 'Generate' button when it is clicked
def handle_button_click(button, tool, temperature, model, user_inputs, user_uploads):
    if button:
        st.markdown("**Response:**")
        chat_box = st.empty()
        stream_handler = StreamHandler(chat_box)
        chat = create_chat(temperature, model, stream_handler)
        if chat and tool:
            try:
                response = tool.execute(chat, *user_inputs, *user_uploads)
                # Save the selected model and temperature along with the response
                response_with_settings = {
                    "response": response,
                    "model": model,
                    "temperature": temperature,
                }
                if "responses" not in st.session_state:
                    st.session_state["responses"] = {}
                if tool.name not in st.session_state["responses"]:
                    st.session_state["responses"][tool.name] = []
                st.session_state["responses"][tool.name].append(response_with_settings)
            except Exception as e:
                st.error(f"An error occurred while executing the tool: {str(e)}")


def handle_tab(tool):
    # Initialize 'responses' in session state if it doesn't exist
    if "responses" not in st.session_state:
        st.session_state["responses"] = {}

    # Create the input fields, advanced options, and the button
    user_uploads = create_data_upload(tool)
    user_inputs = create_input_fields(tool)
    model, temperature = create_advanced_options(tool)
    button = create_generate_button(tool)

    handle_button_click(button, tool, temperature, model, user_inputs, user_uploads)

    # Display the 'Clear Responses' button if there are saved responses for the current tab
    if (
        tool.name in st.session_state["responses"]
        and st.session_state["responses"][tool.name]
    ):
        st.markdown(
            """
                    --- 
                    **Past Responses:**
                    """
        )
        for i, response_with_settings in enumerate(
            st.session_state["responses"].get(tool.name, [])
        ):
            with st.expander(
                f'Response {i+1} - Model: "{response_with_settings["model"]}", Temp: "{response_with_settings["temperature"]}"'
            ):
                st.write(response_with_settings["response"])

        clear_button = st.button(f"Clear Responses for {tool.name}")
        if clear_button:
            # Clear the responses for the current tab
            st.session_state["responses"][tool.name] = []
            clear_button = None
            st.experimental_rerun()
    else:
        clear_button = None


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
