from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


class TemplateType(StrEnum):
    TEMPLATE = "template"
    FILE = "file"
    CONTENT = "content"

    def values():
        return [v for v in TemplateType]


@dataclass(kw_only=True, frozen=True)
class Context:
    cwd: str
    app_name: str
    root: str = field(default=".")
    now: datetime = field(default_factory=datetime.now)


@dataclass(kw_only=True)
class Template:
    name: str
    label: str
    description: str
    variables: dict[str, dict]
    content: dict[str, dict]
    subtemplates: dict[str, dict]
    path: str
    id: int


@dataclass(kw_only=True)
class Subtemplate(Template):
    name: str
    label: str
    description: str
    variables: dict[str, dict]
    content: dict[str, dict]
    path: str
