from typing import Type
from rich import print
from rich.prompt import Prompt


def load_variable(var_name: str, type_: Type = str, preffix: str = " - ") -> Type:
    user_input = Prompt.ask(f"{preffix}[purple]{var_name}[/purple]")
    return type_(user_input)


def load_list(var_name: str, type: Type, prefix: str = " - ") -> list:
    length = Prompt.ask(f"{prefix}[purple]{var_name}[/purple] length")
    length = int(length)
    return [Prompt.ask(f"{prefix}[purple]{var_name}[{i+1}][/purple]") for i in range(length)]

_CALLABLES = {
    str: load_variable,
    int: load_variable,
    float: load_variable,
    bool: load_variable,
    list: load_list
}


def load_variables(prompt: str, description: dict[str, Type], prefix: str = " - ") -> dict:
    if not description:
        return {}
    variables = {}
    print(f"[bold]{prompt}[/bold]")
    for var, type_ in description.items():
        #user_input = Prompt.ask(f"{prefix}[purple]{key}[/purple]")
        variables[var] = _CALLABLES[type_](var, type_, prefix)
    return variables
