class BaseTool:
    def __init__(self, name, model, temperature, file_inputs, inputs):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.file_inputs: dict = file_inputs
        self.inputs: dict = inputs

    def execute(self, chat, tool_registry, *args):
        pass
