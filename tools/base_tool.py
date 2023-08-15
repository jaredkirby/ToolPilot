from typing import List, Dict, Any


class BaseTool:
    def __init__(self, name, model, temperature, inputs, uploads):
        self.name: str = name
        self.model: str = model
        self.temperature: float = temperature
        self.uploads = uploads
        self.inputs: List[Dict[str, Any]] = inputs

    def execute(self, chat, inputs: [Dict[str, Any]], uploads) -> Any:
        pass
