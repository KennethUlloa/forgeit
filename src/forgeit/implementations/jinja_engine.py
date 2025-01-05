from jinja2 import Environment
from ..base import ITemplateEngine


class JinjaTemplateEngine(ITemplateEngine):
    def __init__(self):
        self.env = Environment()

    def render(self, content, data):
        template = self.env.from_string(content)
        return template.render(data)
