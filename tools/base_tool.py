class BaseTool:
    def __init__(self, name, model, temperature, file_inputs, inputs):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.file_inputs = file_inputs
        self.inputs = inputs

    def execute(self, chat, tool_registry, *args):
        pass
