from dataclasses import dataclass, field
from datetime import datetime
from enum import StrEnum


def model(**kwargs):
    return dataclass(kw_only=True, **kwargs)


class TemplateType(StrEnum):
    TEMPLATE = "template"
    FILE = "file"
    CONTENT = "content"

    def values():
        return [v for v in TemplateType]


@model(frozen=True)
class Context:
    cwd: str
    app_name: str
    root: str = field(default=".")
    now: datetime = field(default_factory=datetime.now)


@model()
class BaseTemplate:
    name: str
    label: str
    description: str
    variables: dict[str, dict]
    content: dict[str, str]

    @property
    def path_name(self):
        return self.name


@model()
class Template(BaseTemplate):
    subtemplates: dict[str, dict] = field(default_factory=dict)
    id: int = field(default=None)


@model()
class SubTemplate(BaseTemplate):
    name: str = None
    parent_name: str

    @property
    def path_name(self):
        return self.parent_name


@model()
class Cache:
    template: str
    variables: dict
    root: str


@model()
class TemplateData:
    id: int
    name: str
    description: str
    active: bool
