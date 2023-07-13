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

from secret import OPENAI_API_KEY

openai_api_key = OPENAI_API_KEY
# openai_api_key = st.secrets["OPENAI_API_KEY"]

st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout=LAYOUT)


def create_chat_session(temperature, selected_model, chat_stream_handler):
    try:
        chat_session = ChatOpenAI(
            temperature=temperature,
            model=selected_model,
            openai_api_key=openai_api_key,
            request_timeout=250,
            streaming=True,
            callbacks=[chat_stream_handler],
        )
    except Exception as e:
        st.error(f"An error occurred while creating the chat session: {str(e)}")
        chat_session = None
    return chat_session


def create_tool_input_fields(tool_object):
    tool_user_inputs = []
    for input_field in tool_object.inputs:
        user_input = st.text_area(
            f"Input {input_field['input_label']}",
            input_field["example"],
            key=f"{tool_object.name}_{input_field['input_label']}",
            help=input_field["help_label"],
        )
        tool_user_inputs.append(user_input)
    return tool_user_inputs


def create_tool_advanced_options(tool_object):
    with st.expander("Advanced Options"):
        selected_model = st.selectbox(
            "Select model",
            MODEL,
            key=f"{tool_object.name}_model",
            index=MODEL.index(tool_object.model),
        )
        temp = tool_object.temperature
        selected_temperature = st.slider(
            "Select temperature",
            min_value=0.0,
            max_value=2.0,
            step=0.05,
            value=temp,
            key=f"{tool_object.name}_temp",
        )
    return selected_model, selected_temperature


def create_tool_generate_button(tool_object):
    button_label = "Generate " + " / ".join(
        [input_field["button_label"] for input_field in tool_object.inputs]
    )
    generate_button = st.button(button_label, key=f"{tool_object.name}_button")
    return generate_button


def handle_generate_button_click(
    generate_button, tool_object, selected_temperature, selected_model, tool_user_inputs
):
    if generate_button:
        st.markdown("**Response:**")
        chat_box_placeholder = st.empty()
        chat_stream_handler = StreamHandler(chat_box_placeholder)
        chat_session = create_chat_session(
            selected_temperature, selected_model, chat_stream_handler
        )
        if chat_session and tool_object:
            try:
                tool_response = tool_object.execute(chat_session, *tool_user_inputs)
                tool_response_with_settings = {
                    "response": tool_response,
                    "model": selected_model,
                    "temperature": selected_temperature,
                }
                if "responses" not in st.session_state:
                    st.session_state["responses"] = {}
                if tool_object.name not in st.session_state["responses"]:
                    st.session_state["responses"][tool_object.name] = []
                st.session_state["responses"][tool_object.name].append(
                    tool_response_with_settings
                )
            except Exception as e:
                st.error(f"An error occurred while executing the tool: {str(e)}")


def handle_tool_tab(tool_object):
    if "responses" not in st.session_state:
        st.session_state["responses"] = {}

    tool_user_inputs = create_tool_input_fields(tool_object)
    selected_model, selected_temperature = create_tool_advanced_options(tool_object)
    generate_button = create_tool_generate_button(tool_object)

    handle_generate_button_click(
        generate_button,
        tool_object,
        selected_temperature,
        selected_model,
        tool_user_inputs,
    )

    if (
        tool_object.name in st.session_state["responses"]
        and st.session_state["responses"][tool_object.name]
    ):
        st.markdown(
            """
                    --- 
                    **Past Responses:**
                    """
        )
        for i, tool_response_with_settings in enumerate(
            st.session_state["responses"].get(tool_object.name, [])
        ):
            with st.expander(
                f'Response {i+1} - Model: "{tool_response_with_settings["model"]}", Temp: "{tool_response_with_settings["temperature"]}"'
            ):
                st.write(tool_response_with_settings["response"])

        clear_responses_button = st.button(f"Clear Responses for {tool_object.name}")
        if clear_responses_button:
            st.session_state["responses"][tool_object.name] = []
            clear_responses_button = None
            st.experimental_rerun()
    else:
        clear_responses_button = None


def streamlit_app_main():
    st.markdown(
        f"<h1 style='text-align: center;'>{PAGE_TITLE} {PAGE_ICON} <br> {SUB_TITLE}</h1>",
        unsafe_allow_html=True,
    )

    # Create a selectbox for selecting the group of tools
    group_names = list(TOOL_REGISTRY.keys())
    selected_group_name = st.selectbox("Select a group of tools:", group_names)
    selected_group = TOOL_REGISTRY[selected_group_name]

    # Get the names of the tools in the selected group
    tool_names = list(selected_group.keys())

    tab_ui_elements = st.tabs(tool_names)

    for tab_ui_element, tool_name in zip(tab_ui_elements, tool_names):
        with tab_ui_element:
            handle_tool_tab(selected_group[tool_name])

    st.markdown(
        """
    ---
    Built by **Jared Kirby** :wave:

    [Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

        """
    )


if __name__ == "__main__":
    streamlit_app_main()
