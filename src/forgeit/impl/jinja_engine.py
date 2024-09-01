import jinja2
from ..domain.engine import ITemplateEngine


class Jinja2Engine(ITemplateEngine):
    def __init__(self):
        self.env = jinja2.Environment()

    def render_string(self, content: str, data: dict) -> str:
        template = self.env.from_string(content)
        return template.render(data)
