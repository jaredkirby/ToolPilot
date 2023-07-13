# tool.py
import streamlit as st

from config import MODEL


class Tool:
    def __init__(self, tool_object, openai_api_key):
        self.tool_object = tool_object
        self.selected_model = tool_object.models[0]
        self.selected_temperature = None  # Add this line
        self.openai_api_key = openai_api_key

    def create_input_fields(self):
        tool_user_inputs = []
        for input_field in self.tool_object.inputs:
            user_input = st.text_area(
                f"Input {input_field['input_label']}",
                input_field["example"],
                key=f"{self.tool_object.name}_{input_field['input_label']}",
                help=input_field["help_label"],
            )
            tool_user_inputs.append(user_input)
        return tool_user_inputs

    def create_advanced_options(self):
        with st.expander("Advanced Options"):
            selected_model = st.selectbox(
                "Select model",
                MODEL,
                key=f"{self.tool_object.name}_model",
                index=MODEL.index(self.tool_object.model),
            )
            temp = self.tool_object.temperature
            selected_temperature = st.slider(
                "Select temperature",
                min_value=0.0,
                max_value=2.0,
                step=0.05,
                value=temp,
                key=f"{self.tool_object.name}_temp",
            )
        return selected_model, selected_temperature

    def create_generate_button(self):
        button_label = "Generate " + " / ".join(
            [input_field["button_label"] for input_field in self.tool_object.inputs]
        )
        generate_button = st.button(button_label, key=f"{self.tool_object.name}_button")
        return generate_button

    # ... remaining methods ...
