from typing import Type
from rich import print
from rich.prompt import Prompt, Confirm


def load_variable(var_name: str, type_: Type = str, preffix: str = " - ") -> Type:
    user_input = Prompt.ask(f"{preffix}[purple]{var_name}[/purple]")
    return type_(user_input)

def load_list(var_name: str, _, prefix: str = " - ") -> list:
    length = Prompt.ask(f"{prefix}[purple]{var_name}[/purple] length")
    length = int(length)
    return [Prompt.ask(f"{prefix}[purple]{var_name}[{i+1}][/purple]") for i in range(length)]

def load_boolean(var_name: str, _, prefix: str = " - ") -> bool:
    return Confirm.ask(f"{prefix}[purple]{var_name}[/purple]") 


def load_variables(prompt: str, vars_description: dict[str, Type], preffix: str = " - ") -> dict:
    if not vars_description:
        return {}
    variables = {}
    print(f"[bold]{prompt}[/bold]")
    for name, type_ in vars_description.items():
        # TODO: List variables support
        # TODO: Smart type checking in case of callbacks to select input function
        variables[name] = load_variable(name, type_, preffix)
    return variables
