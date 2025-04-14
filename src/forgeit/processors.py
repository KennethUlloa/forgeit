from datetime import datetime
from typing import Callable


processors = {}
tests = {}


def filter(key: str = None):
    def decorator(f: Callable):
        name = key or f.__name__
        processors[name] = f
        return f

    return decorator


def test(key: str = None):
    def decorator(f: Callable):
        name = key or f.__name__
        tests[name] = f
        return f

    return decorator


@filter()
def camel_case(content: str):
    content = content.replace("_", " ").replace("-", " ")
    words = content.split(" ")
    return words[0].lower() + "".join(word.title() for word in words[1:])


@filter()
def kebab_case(content: str):
    return content.lower().replace(" ", "-").replace("_", "-")


@filter()
def snake_case(content: str):
    return content.lower().replace(" ", "_").replace("-", "_")


@filter()
def pascal_case(content: str):
    return content.title().replace(" ", "").replace("_", "").replace("-", "")


@filter()
def uniques(value: list):
    return set(value)


@filter()
def key_values(value: list, name: str):
    def get_value(obj, name):
        if isinstance(obj, dict):
            return obj.get(name)
        if hasattr(obj, name):
            return getattr(obj, name)
        return None

    return [get_value(v, name) for v in value]


@filter()
def format_date(value: datetime, format: str):
    return value.strftime(format)


@filter()
def included(value: list, targets: list):
    return [v for v in value if v in targets]


@filter()
def symbol(value: str):
    return value.split(".")[-1]


@filter()
def module_path(value: str):
    parts = value.split(".")[0:-1]
    return ".".join(parts)
