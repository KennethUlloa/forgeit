from abc import ABC, abstractmethod

class VariableProcessor(ABC):
    def __init__(self, var_name: str, target_name: str = None):
        self.var_name = var_name
        self.target_name = target_name or var_name
    
    def __call__(self, data: dict) -> dict:
        data[self.target_name] = self.process(data[self.var_name])
        return data
    
    @abstractmethod
    def process(self, content: str) -> str:
        raise NotImplementedError()

class CamelCaseProcessor(VariableProcessor):
    def process(self, content: str) -> str:
        content = content.replace("_", " ").replace("-", " ")
        words = content.split(" ")
        return words[0] + "".join(word.title() for word in words[1:])
    
class SnakeCaseProcessor(VariableProcessor):
    def process(self, content: str) -> str:
        return content.lower().replace(" ", "_").replace("-", "_")
    
class KebabCaseProcessor(VariableProcessor):
    def process(self, content: str) -> str:
        return content.lower().replace(" ", "-").replace("_", "-")

class PascalCaseProcessor(VariableProcessor):
    def process(self, content: str) -> str:
        return content.title().replace(" ", "").replace("_", "").replace("-", "")
