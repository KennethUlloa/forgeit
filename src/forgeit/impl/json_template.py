from typing import Type
from ..domain.template import Template
from ..domain.processor import (
    Processor, 
    CamelCaseProcessor, 
    SnakeCaseProcessor, 
    KebabCaseProcessor, 
    PascalCaseProcessor)


PROCESSORS_MAP: dict[str, Type[Processor]] = {
    "camel": CamelCaseProcessor,
    "snake": SnakeCaseProcessor,
    "kebab": KebabCaseProcessor,
    "pascal": PascalCaseProcessor
}


TYPE_MAP = {
    "str": str,
    "int": int,
    "float": float,
    "bool": bool
}

def map_processor(data: dict, target: str) -> dict:
    processor = PROCESSORS_MAP[data["name"]]
    return processor(data["var"], target)


def map_template(data: dict) -> Template:
    
    return Template(
        name=data["name"],
        description=data["description"],
        variables={key: TYPE_MAP[value] for key, value in data["variables"].items()},
        src=data["src"],
        exclude=data.get("exclude", []),
        processors={key: map_processor(value, key) for key, value in data.get("processors", {}).items()}
    )
