import importlib
import importlib.util
from dataclasses import dataclass, field
from .engine import ITemplateEngine
from .template import ITemplate


@dataclass(kw_only=True)
class Config:
    ENGINE: ITemplateEngine = None
    ENCODING: str = "utf-8"
    TEMPLATES: dict[str, ITemplate] = field(default_factory=dict)


config = Config()


def load_object(object) -> Config:
    if isinstance(object, dict):
        config.TEMPLATES.update(object.get("TEMPLATES", {}))
        config.ENCODING = object.get("ENCODING", "utf-8")
        config.ENGINE = object.get("ENGINE")
    else:
        config.TEMPLATES.update(getattr(object, "TEMPLATES", {}))
        config.ENCODING = getattr(object, "ENCODING", "utf-8")
        config.ENGINE = getattr(object, "ENGINE")
    return config


def load_module(module_path: str) -> Config:
    module = importlib.import_module(module_path)
    return load_object(module)


def load_py(file_path: str) -> Config:
    module_name = "config_" + file_path.lower().replace("\\", "_").replace(
        "/", "_"
    ).replace("-", "_")
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return load_module(module)
