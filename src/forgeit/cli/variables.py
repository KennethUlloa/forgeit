from typing import Type
from rich import print
from rich.prompt import Prompt


def load_variables(prompt: str, description: dict[str, Type], prefix: str = " - ") -> dict:
    if not description:
        return {}
    variables = {}
    print(f"[bold]{prompt}[/bold]")
    for key, value in description.items():
        user_input = Prompt.ask(f"{prefix}[purple]{key}[/purple]")
        variables[key] = value(user_input)
    return variables
