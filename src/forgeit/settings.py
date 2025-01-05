import os
import pathlib
import importlib.util
from .base import ITemplate, ITemplateEngine
from .implementations.jinja_engine import JinjaTemplateEngine

global_path = os.path.join(pathlib.Path.home(), ".forgeit", "forge_settings.py")


class Setting:
    TEMPLATES: dict[str, ITemplate] = {}
    ENGINE: ITemplateEngine = JinjaTemplateEngine()
    ENCODING: str = "utf-8"

    @classmethod
    def load_from_module(cls, module):
        cls.ENGINE = getattr(module, "ENGINE", JinjaTemplateEngine())
        cls.ENCODING = getattr(module, "ENCODING", "utf-8")
        templates = getattr(module, "TEMPLATES")
        cls.TEMPLATES.update(templates)

    @classmethod
    def load_from_file(cls, path: str, check_exists: bool = False):
        if check_exists and not os.path.exists(path):
            return
        spec = importlib.util.spec_from_file_location("custom_config", path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.load_from_module(module)

    @classmethod
    def load_global(cls):
        try:
            cls.load_from_file(global_path, True)
        except Exception:
            pass
