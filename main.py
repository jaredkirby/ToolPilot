import streamlit as st

from langchain.chat_models import ChatOpenAI

from utils.stream import StreamHandler
import tools.dos as dos
import tools.pilot as pilot
import tools.instruct as instruct
import tools.purpose as purpose
import tools.resume as resume

# from secret import OPENAI_API_KEY

# openai_api_key = OPENAI_API_KEY
openai_api_key = st.secrets["OPENAI_API_KEY"]

PAGE_TITLE = "PromptPilot"
PAGE_ICON = "🛠️"
SUB_TITLE = "Tools for Prompting LLMs"
LAYOUT = "centered"
MODEL = [
    "gpt-4",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-16k",
]
TEMPERATURE = {
    "Discipline of Study": 0.75,
    "PromptPilot": 1.0,
    "Improve Prompt Instructions": 1.0,
    "Prompt Purpose": 0.75,
    "Resume": 0.75,
}
TOOL_FUNCTIONS = {
    "Discipline of Study": dos.get_dos_response,
    "PromptPilot": pilot.get_pilot_response,
    "Improve Prompt Instructions": instruct.get_instruct_response,
    "Prompt Purpose": purpose.get_purpose_response,
    "Resume": resume.get_resume_response,
}
DOS = "Discipline of Study"
PILOT = "PromptPilot"
INSTRUCT = "Improve Prompt Instructions"
PURPOSE = "Prompt Purpose"
RESUME = "Resume"

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


def handle_tab(tab_name, samples, button_labels, input_labels, help_labels):
    # Get example input for the given tab
    sample = samples.get(tab_name)

    # Get the label to be displayed on the input field for the given tab
    input_label = input_labels.get(tab_name)

    # Get the help text to be displayed with the input field for the given tab
    help_label = help_labels.get(tab_name)

    # Create an input text area with a label, example text and help text specific to the given tab
    user_input = st.text_area(
        f"Input {input_label}", sample, key=f"{tab_name}_input", help=help_label
    )
    if tab_name == RESUME:
        user_input_two = st.text_area(
            "Input Resume", key=f"{tab_name}_input_two", help=help_label
        )

    # Create a section for advanced options
    with st.expander("Advanced Options"):
        # Allow user to select a model from a dropdown
        model = st.selectbox("Select model", MODEL, key=f"{tab_name}_model")

        # Get the default 'temperature' parameter for the selected model
        temp = TEMPERATURE.get(tab_name)

        # Allow user to adjust the 'temperature' parameter using a slider
        temperature = st.slider(
            "Select temperature",
            min_value=0.0,
            max_value=2.0,
            step=0.05,
            value=temp,
            key=f"{tab_name}_temp",
        )

    # Get the label to be displayed on the 'Generate' button for the given tab
    button_label = button_labels.get(tab_name)

    # Create a 'Generate' button with a label specific to the given tab
    button = st.button(f"Generate {button_label}", key=f"{tab_name}_button")

    # If the 'Generate' button is clicked
    if button:
        # Create an empty chat box
        chat_box = st.empty()

        # Initialize the stream handler with the chat box
        stream_handler = StreamHandler(chat_box)

        # Initialize a chat session with the selected temperature and model, and the stream handler
        chat = create_chat(temperature, model, stream_handler)

        # Get the function associated with the given tab
        function = TOOL_FUNCTIONS.get(tab_name)

        # If there is a function associated with the tab, execute it with the chat and user_input as parameters
        if function:
            function(chat, user_input, user_input_two)


def main():
    st.markdown(
        f"<h1 style='text-align: center;'>{PAGE_TITLE} {PAGE_ICON} <br> {SUB_TITLE}</h1>",
        unsafe_allow_html=True,
    )

    # Define the examples dictionary
    examples = {
        DOS: "Youtube video writer and editor for a DIY Entrepreneurs focused channel",
        PILOT: "Plan, write, and edit scripts for Youtube videos",
        INSTRUCT: "Write and edit scripts for Youtube videos",
        PURPOSE: "Write and edit scripts for Youtube videos",
        RESUME: "",
    }

    # Define the button label dictionary
    button_labels = {
        DOS: "Discipline",
        PILOT: "Prompt",
        INSTRUCT: "Instructions",
        PURPOSE: "Purpose",
        RESUME: "Resume",
    }

    # Define the input label dictionary
    input_labels = {
        DOS: "Topic or Objective",
        PILOT: "Original Prompt",
        INSTRUCT: "Original Instructions",
        PURPOSE: "Prompt",
        RESUME: "Job Description",
    }

    # Define the help label dictionary
    help_labels = {
        DOS: 'This tool helps you generate a prompt intro that focus the language model on a particular area of its training. Example: If you want to ask a question about the benefits of exercise, you might use this tool by giving the topics "exercise" and "health".',
        PILOT: 'The PromptPilot tool helps you generate a prompt that meets the best practices of prompt engineering. For example, if you want to ask a question about the benefits of exercise, you could input the prompt "What is the best exercise program for people over the age of 40?"',
        INSTRUCT: "The Improve Prompt Instructions tool helps you generate a prompt that provides clear instructions for the language model. For example, if you want to generate a specific exercise program, you could input the instructions'Generate a 12-week exercise program for people over the age of 40 and include a list of exercises, sets, and reps for each day of the week.",
        PURPOSE: "The Prompt Purpose tool helps by reviewing a given prompt and generating a summary of the prompt's purpose.",
        RESUME: "The Resume tool helps by reviewing a given resume and job description and generates an optimized version.",
    }

    # Set up tabs
    tabs = [
        DOS,
        PILOT,
        INSTRUCT,
        PURPOSE,
        RESUME,
    ]

    tab1, tab2, tab3, tab4, tab5 = st.tabs(tabs)

    with tab1:
        handle_tab(tabs[0], examples, button_labels, input_labels, help_labels)
    with tab2:
        handle_tab(tabs[1], examples, button_labels, input_labels, help_labels)
    with tab3:
        handle_tab(tabs[2], examples, button_labels, input_labels, help_labels)
    with tab4:
        handle_tab(tabs[3], examples, button_labels, input_labels, help_labels)
    with tab5:
        handle_tab(tabs[4], examples, button_labels, input_labels, help_labels)

    st.markdown(
        """
    ---
    Built by **Jared Kirby** :wave:

    [Twitter](https://twitter.com/Kirby_) | [GitHub](https://github.com/jaredkirby) | [LinkedIn](https://www.linkedin.com/in/jared-kirby/) | [Portfolio](https://www.jaredkirby.me)

        """
    )


if __name__ == "__main__":
    main()
