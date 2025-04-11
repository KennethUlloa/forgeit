import os
from jinja2 import Environment, FileSystemLoader
from .processors import processors


class Engine:
    def __init__(self, path: str):
        template_path = os.path.realpath(path)

        if os.path.isfile(template_path):
            print("is file")
            template_path = os.path.dirname(template_path)

        self.__engine = Environment(
            loader=FileSystemLoader(os.path.join(template_path, "templates"))
        )
        self.__engine.filters.update(processors)

    def render_file(self, path: str, data: dict) -> str:
        template = self.__engine.get_template(path)
        return template.render(data)

    def render_string(self, string: str, data: dict) -> str:
        template = self.__engine.from_string(string)
        return template.render(data)
