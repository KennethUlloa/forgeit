import os
from forgeit.application import Forge
from forgeit.impl import fs_content_reader, jinja_engine, local_template_repository


VERSION="0.1.0"


def default() -> Forge:
    return Forge(
        fs_content_reader.FSContentHandler(),
        jinja_engine.Jinja2Engine(),
        local_template_repository.LocalTemplateRepository(os.getenv("FORGE_CONFIG_PATH", "forge.config.json"))
    )
