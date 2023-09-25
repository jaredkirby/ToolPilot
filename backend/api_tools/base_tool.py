from abc import ABC, abstractmethod
from typing import List, Dict, Any

from ..utils import create_chat


class BaseTool(ABC):
    def __init__(self, name, model, temperature, uploads=None, inputs=None):
        self.name: str = name
        self.model: str = model
        self.temperature: float = temperature
        self.uploads = uploads
        self.inputs: List[Dict[str, Any]] = inputs if inputs else []
        self.chat = create_chat(self.temperature, self.model)

    @abstractmethod
    def execute(self, *args, **kwargs) -> Any:
        pass
