from typing import Type
from inspect import signature
from rich import print
from rich.prompt import Prompt, Confirm, IntPrompt, FloatPrompt


def format_variable_name(name: str):
    return name.replace("_", " ").replace("-", " ").capitalize().strip()


def load_list(
    var_name: str, prefix: str = " * ", level: int = 0, spacer: str = " "
) -> list:
    length = IntPrompt.ask(
        f"{spacer * level}{prefix}[yellow]{format_variable_name(var_name)}[/yellow] length"
    )
    return [
        Prompt.ask(f"{spacer * (level + 1)}[yellow]({i+1})[/yellow]")
        for i in range(length)
    ]


def load_primitive(name: str, type_: Type, prefix: str, level: int, spacer: str):
    if issubclass(type_, bool):
        return Confirm.ask(
            f"{spacer * level}{prefix}[purple]{format_variable_name(name)}?[/purple]"
        )

    if issubclass(type_, int):
        return IntPrompt.ask(
            f"{spacer * level}{prefix}[cyan]{format_variable_name(name)}[/cyan]"
        )
    
    if issubclass(type_, float):
        return FloatPrompt.ask(
            f"{spacer * level}{prefix}[cyan]{format_variable_name(name)}[/cyan]"
        )

    return Prompt.ask(
        f"{spacer * level}{prefix}[bold]{format_variable_name(name)}[/bold]"
    )


def load_type(name: str, type_: Type, prefix: str, level: int, spacer: str):
    data = {
        p_name: parameter.annotation
        for p_name, parameter in signature(type_).parameters.items()
        if parameter.annotation != parameter.empty
    }
    kwargs = load_dict(name, data, prefix, level, spacer)
    return type_(**kwargs)


def load_dict(
    name: str, data: dict, prefix: str = " * ", level: int = 0, spacer: str = " "
):
    values = {}
    if name:
        print(f"{spacer * level}{prefix}[green]{format_variable_name(name)}[/green]")
    child_level = level + 1
    for key, val in data.items():
        if isinstance(val, dict):
            values[key] = load_dict(key, val, prefix, child_level, spacer)
        elif issubclass(val, list):
            values[key] = load_list(key, prefix, child_level, spacer)
        elif issubclass(val, (str, int, float, bool)):
            values[key] = load_primitive(key, val, prefix, child_level, spacer)
        else:
            values[key] = load_type(key, val, prefix, child_level, spacer)
    return values


def load_variables(
    data: dict[str, Type],
    prefix: str = "* ",
    spacer: str = "  ",
) -> dict:
    return load_dict(None, data, prefix, -1, spacer)
