import os
import json
from ..domain.template import Template, ITemplateRepository
from .json_template import map_template


class LocalTemplateRepository(ITemplateRepository):
    """
    This class is responsible for loading the templates from a local file.

    All the paths of the templates are relative to the configuration file.
    """
    _templates: dict[str, Template]
    path: str

    def __init__(self, config_path: str):
        if not config_path:
            raise ValueError("Config path not provided")
        
        if not os.path.exists(config_path):
            raise FileNotFoundError("Config file not found")
        
        self._templates = {}
        with open(config_path, "r") as file:
            data = json.load(file)
        
        if "path" in data:
            self.path = data["path"]
        else:
            self.path = os.path.dirname(config_path)

        self._load_templates(data["templates"])

    def get_template(self, name: str) -> Template:
        return self._templates[name]

    def list_templates(self) -> list[Template]:
        return list(self._templates.values())
    
    def _load_templates(self, data: list[dict]):
        for template_dict in data:
            template = map_template(template_dict)
            template.src = os.path.join(self.path, template.src)
            self._templates[template_dict["name"]] = template
