from ..domain.content import IContentHandler
from ..domain.engine import ITemplateEngine
from ..domain.template import Template, ITemplateRepository

class Forge:
    _content_handler: IContentHandler
    _engine: ITemplateEngine
    _template_repository: ITemplateRepository

    def __init__(self, content_handler: IContentHandler, engine: ITemplateEngine, template_repository: ITemplateRepository):
        self._content_handler = content_handler
        self._engine = engine
        self._template_repository = template_repository

    def render_template(self, template: str | Template, path: str, data: dict):
        if isinstance(template, str):
            template = self._template_repository.get_template(template)
        return template.render(path, data, self._engine, self._content_handler)

    def templates_dict(self) -> dict[str, Template]:
        return {template.name: template for template in self._template_repository.list_templates()}
    
    def templates_list(self) -> list[Template]:
        return self._template_repository.list_templates()

    def get_template(self, name: str) -> Template:
        return self._template_repository.get_template(name)
