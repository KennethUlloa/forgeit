import re
import rich
from typing import Callable
from rich.prompt import Prompt, IntPrompt, FloatPrompt, Confirm


"""

typeof = type


class VariableType(ABC):
    type: str

    def __init__(self, *, name: str, label: str = None, **_):
        self.name = name
        self.label = label

    @abstractmethod
    def request_input(self, parent_spacer: str):
        pass


class VariableTypeStore:
    bindings: dict[str, Type[VariableType]] = {}

    @classmethod
    def get(cls, typeName: str):
        return cls.bindings[typeName]

    @classmethod
    def has(cls, typeName: str):
        return typeName in cls.bindings


class StringType(VariableType):
    type = "string"

    def __init__(self, *, name, label=None, allow_empty: bool = True, **_):
        super().__init__(name=name, label=label, **_)
        self.allow_empty = allow_empty

    def request_input(self, parent_spacer: str):
        label = self.label or self.name.capitalize()
        content = Prompt.ask(f"{parent_spacer}{label}")
        if not self.allow_empty and not content:
            log(f"{parent_spacer}Empty strings not allowed")
        while not self.allow_empty and not content:
            content = Prompt.ask(f"{parent_spacer}{label}")
            if not content:
                log(f"{parent_spacer}Empty strings not allowed")
        return content


class IntegerType(VariableType):
    type = "integer"

    def __init__(self, *, name, label=None, **_):
        super().__init__(name=name, label=label, **_)

    def request_input(self, parent_spacer: str):
        label = self.label or self.name.capitalize()
        return IntPrompt.ask(f"{parent_spacer}{label}")


class FloatType(VariableType):
    type = "float"

    def __init__(self, *, name, label=None, **_):
        super().__init__(name=name, label=label, **_)

    def request_input(self, parent_spacer: str):
        label = self.label or self.name.capitalize()
        return FloatPrompt.ask(f"{parent_spacer}{label}")


class BooleanType(VariableType):
    type = "boolean"

    def __init__(self, *, name, label=None, **_):
        super().__init__(name=name, label=label, **_)

    def request_input(self, parent_spacer: str):
        label = self.label or self.name.capitalize()
        return Confirm.ask(f"{parent_spacer}{label}")


class ListType(VariableType):
    type = "list"

    def __init__(
        self,
        *,
        item_attributes: dict,
        size: int = None,
        **kwargs,
    ):
        super().__init__(**kwargs)
        self.item_attributes = item_attributes
        self.size = max(0, int(size)) if size is not None else size

    def request_input(self, parent_spacer: str):
        if self.size == 0:
            return []

        items = []
        label = self.label or self.name.capitalize()
        log(
            f"{parent_spacer}[yellow]{label} ({'list' if self.size is None else self.size})[/yellow]"
        )
        item_type = VariableTypeStore.get(self.item_attributes["type"])
        item_label = self.item_attributes.get("label") or ""
        if item_label:
            item_label += " "
        add_more_items = True

        while add_more_items:
            item_attrs = {**self.item_attributes}
            item_attrs["label"] = f"{item_label}[{len(items)}]"
            item_attrs["name"] = ""
            item = item_type(**item_attrs)
            items.append(item.request_input(parent_spacer + "  "))
            if self.size is None:
                add_more_items = Confirm.ask(f"{parent_spacer}  Add more?")
                continue

            if len(items) == self.size:
                break

        return items


class ObjectType(VariableType):
    type = "object"

    def __init__(self, *, name: str, label: str = None, props: dict, **kwargs):
        super().__init__(name=name, label=label, **kwargs)
        self.props = props

    def request_input(self, parent_spacer: str):
        label = self.label or self.name.capitalize()
        log(f"{parent_spacer}[green]{label} (object)[/green]")
        item = {}
        for name, prop in self.props.items():
            item_type = VariableTypeStore.get(prop["type"])
            prop["name"] = name
            item[name] = item_type(**prop).request_input(parent_spacer + "  ")

        return item


VariableTypeStore.bindings = {
    t.type: t
    for t in [StringType, IntegerType, FloatType, BooleanType, ListType, ObjectType]
}

"""

class Registry:
    __types: dict[str, Callable] = {}

    @classmethod
    def get(cls, key: str) -> Callable:
        return cls.__types[key]

    @classmethod
    def set(cls, key: str, func: Callable) -> Callable:
        cls.__types[key] = func


def register(key: str):
    def decorator(f):
        Registry.set(key, f)
        return f

    return decorator


@register("object")
def object_input(*, label: str, props: dict, parent_space: str = "", **_):
    prompt = f"{parent_space}{label} [green](object)[/green]"
    rich.print(prompt)

    obj = {}

    for key, value in props.items():
        obj[key] = Registry.get(value["type"])(
            **value, parent_space=parent_space + "  "
        )

    return obj


@register("list")
def list_input(
    *,
    label: str,
    item_type: str,
    item_attributes: dict,
    size: int = None,
    parent_space: str = "",
    continue_prompt: str = "Continue?",
    continue_default: bool = False,
    **_,
):
    prompt = f"{parent_space}{label} [yellow](list{f':{size}' if size is not None else ''})[/yellow]"
    item_type: Callable = Registry.get(item_type)
    items = []
    rich.print(prompt)
    while True:
        current_item_attrs = {**item_attributes}
        current_item_attrs["label"] = item_attributes["label"].replace(
            "{i}", str(len(items))
        )

        items.append(item_type(**current_item_attrs, parent_space=parent_space + "  "))

        if size is None:
            if not Confirm.ask(
                f"{parent_space}{continue_prompt}",
                default=continue_default,
                show_default=True,
            ):
                break
            continue

        if len(items) == size:
            break

    return items


@register("string")
def str_input(
    *,
    label: str,
    min_length: int = None,
    max_length: int = None,
    regex: str = None,
    default: str = None,
    password: bool = False,
    choices: list[str] = None,
    parent_space: str = "",
    **_,
):
    prompt = label
    if regex is not None:
        pattern = re.compile(regex)

    if choices is None:
        if min_length is not None and max_length is not None:
            prompt = f"{label} ({min_length} to {max_length} characters)"

        elif min_length is not None:
            prompt = f"{label} ({min_length} characters minimum)"

        elif max_length is not None:
            prompt = f"{label} ({max_length} characters maximum)"

    regex_escaped = regex.replace("[", "\\[") if regex else ""
    while True:
        value = Prompt.ask(
            f"{parent_space}{prompt} [cyan](string)[/cyan]",
            default=default,
            show_default=True,
            choices=choices,
            show_choices=True,
            password=password,
        )

        # Choices have precedence to inline validations
        if choices is not None:
            break

        if regex is not None and pattern.fullmatch(value) is None:
            rich.print(f"{parent_space}[red]Input doesn't match {regex_escaped}[/red]")
            continue

        if max_length is not None and len(value) > max_length:
            rich.print(f"{parent_space}[red]{max_length} characters maximum[/red]")
            continue

        if min_length is not None and len(value) < min_length:
            rich.print(f"{parent_space}[red]{min_length} characters minimum[/red]")
            continue

        break

    return value


@register("integer")
def int_input(
    *,
    label: str,
    min_value: int = None,
    max_value: int = None,
    default: int = None,
    parent_space: str = "",
    **_,
):
    prompt = label

    if min_value is not None and max_value is not None:
        prompt = f"{label} ({min_value} to {max_value})"

    elif min_value is not None:
        prompt = f"{label} (>= {min_value})"

    elif max_value is not None:
        prompt = f"{label} (<= {max_value})"

    while True:
        value = IntPrompt.ask(
            f"{parent_space}{prompt} [cyan](integer)[/cyan]",
            show_default=True,
            default=default,
        )

        if value is None:
            rich.print(f"{parent_space}[red]Please enter a number[red/]")
            continue

        if min_value is not None and value < min_value:
            rich.print(f"{parent_space}[red]{value} is less than {min_value}[red/]")
            continue

        if max_value is not None and value > max_value:
            rich.print(f"{parent_space}[red]{value} is greater than {max_value}[red/]")
            continue

        break

    return value


@register("float")
def float_input(
    *,
    label: str,
    min_value: float = None,
    max_value: float = None,
    default: float = None,
    parent_space: str = "",
    **_,
):
    prompt = label

    if min_value is not None and max_value is not None:
        prompt = f"{label} ({min_value} to {max_value})"

    elif min_value is not None:
        prompt = f"{label} (>= {min_value})"

    elif max_value is not None:
        prompt = f"{label} (<={max_value})"

    while True:
        value = FloatPrompt.ask(
            f"{parent_space}{prompt} [cyan](float)[/cyan]",
            show_default=True,
            default=default,
        )

        if value is None:
            rich.print(f"{parent_space}[red]Please enter a number[red/]")
            continue

        if min_value is not None and value < min_value:
            rich.print(f"{parent_space}[red]{value} is less than {min_value}[red/]")
            continue

        if max_value is not None and value > max_value:
            rich.print(f"{parent_space}[red]{value} is greater than {max_value}[red/]")
            continue

        break

    return value


@register("boolean")
def bool_input(*, label: str, default: bool = None, parent_space: str = "", **_):
    return Confirm.ask(f"{parent_space}{label}?", show_default=True, default=default)