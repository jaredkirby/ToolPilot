class BaseTool:
    def __init__(self, name, model, temperature, inputs):
        self.name = name
        self.model = model
        self.temperature = temperature
        self.inputs = inputs

    def execute(self, chat, tool_registry, *args):
        pass
