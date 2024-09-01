from typing import Type


class Processor[T]:
    def __init__(self, var: str, target: str):
        self.var = var
        self.target = target

    def process(self, data: T) -> T:
        raise NotImplementedError("Method not implemented")
    

class CamelCaseProcessor(Processor[str]):
    def process(self, data: str) -> str:
        data = data.replace("_", " ").replace("-", " ")
        words = data.split(" ")
        return words[0] + "".join(word.title() for word in words[1:])
    
class SnakeCaseProcessor(Processor[str]):
    def process(self, data: str) -> str:
        return data.lower().replace(" ", "_").replace("-", "_")
    
class KebabCaseProcessor(Processor[str]):
    def process(self, data: str) -> str:
        return data.lower().replace(" ", "-").replace("_", "-")
    
class PascalCaseProcessor(Processor[str]):
    def process(self, data: str) -> str:
        return data.title().replace(" ", "").replace("_", "").replace("-", "")
