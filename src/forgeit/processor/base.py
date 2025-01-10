from abc import ABC, abstractmethod
from ..utils.data import read, save

class VariableProcessor(ABC):
    def __init__(self, var_name: str, target_name: str):
        self.var_name = var_name
        self.target_name = target_name
    
    def __call__(self, data: dict) -> dict:
        return save(self.target_name, self.process(read(self.var_name)(data)))(data)
    
    @abstractmethod
    def process(self, content: str) -> str:
        raise NotImplementedError()

class CamelCase(VariableProcessor):
    def process(self, content: str) -> str:
        content = content.replace("_", " ").replace("-", " ")
        words = content.split(" ")
        return words[0] + "".join(word.title() for word in words[1:])
    
class SnakeCase(VariableProcessor):
    def process(self, content: str) -> str:
        return content.lower().replace(" ", "_").replace("-", "_")
    
class KebabCase(VariableProcessor):
    def process(self, content: str) -> str:
        return content.lower().replace(" ", "-").replace("_", "-")

class PascalCase(VariableProcessor):
    def process(self, content: str) -> str:
        return content.title().replace(" ", "").replace("_", "").replace("-", "")

__all__ = ["VariableProcessor", "CamelCase", "SnakeCase", "KebabCase", "PascalCase"]