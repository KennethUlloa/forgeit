import os
from jinja2 import Environment, FileSystemLoader
from .processors import processors


class RenderEngine:
    def __init__(self, path: str):
        self.__engine = Environment(loader=FileSystemLoader(path))
        self.__engine.filters.update(processors)

    def render_file(self, path: str, data: dict) -> str:
        template = self.__engine.get_template(path)
        return template.render(data)

    def render_string(self, string: str, data: dict) -> str:
        template = self.__engine.from_string(string)
        return template.render(data)
