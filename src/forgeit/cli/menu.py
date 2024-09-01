from typing import Callable
from rich import print
from rich.prompt import Prompt



class IndexMenu:
    def __init__(self, elements: list, formatter: Callable, prefix: str = " - "):
        self.elements = elements
        self.formatter = formatter
        self.prefix = prefix

    def show(self, prompt: str = "Select an option"):
        print(prompt)
        for index, element in enumerate(self.elements):
            print(f"{self.prefix}{index + 1}. {self.formatter(element)}")
        
        selected_index = Prompt.ask(
            "[yellow]Select an option[/yellow]", 
            choices=[str(i + 1) for i in range(len(self.elements))], show_choices=False)
        
        return self.elements[int(selected_index) - 1]


class KeyMenu:
    def __init__(self, elements: dict, formatter: Callable, prefix: str = " - "):
        self.elements = elements
        self.formatter = formatter
        self.prefix = prefix

    def show(self):
        for key, element in self.elements.items():
            print(f"{self.prefix}{key}. {self.formatter(element)}")
        
        selected_key = Prompt.ask(
            "Select an option", 
            choices=[str(k) for k in self.elements.keys()], show_choices=False)
        
        return self.elements[selected_key]
