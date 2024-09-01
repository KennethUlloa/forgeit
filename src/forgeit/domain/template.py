import os
from abc import ABC, abstractmethod
from typing import Type

from ..domain.processor import Processor
from ..utils.files import match_pattern
from .engine import ITemplateEngine
from .content import IContentHandler


class ProcessorInfo:
    name: str
    var: str

    def __init__(self, name: str, var: str):
        self.name = name
        self.var = var


class Template:
    """
    Template class that represents a template to be rendered. A template is defined by a name, a description, a set of
    variables and a folder containing the template files.
    """
    name: str
    description: str
    variables: dict[str, Type]
    src: str
    exclude: list[str]
    processors: dict[str, Processor]

    def __init__(self, name: str, description: str, variables: dict, src: str, exclude: list = [], processors: dict = {}):
        self.name = name
        self.description = description
        self.variables = variables
        self.src = src
        self.exclude = exclude
        self.processors = processors

    def render(self, path: str, data: dict, engine: ITemplateEngine, content_handler: IContentHandler) -> list[str]:
        """
        Render the template with the given context data.

        :param data: The context data
        :param engine: The template engine
        """

        if not self.validate_data(data):
            raise ValueError("Invalid data")

        for key, processor in self.processors.items():
            data[key] = processor.process(data[processor.var])
        
        rendered_files = []

        for file, relative in content_handler.list_files(self.src):
            # Skip the file if it matches the exclude patterns
            if match_pattern(file, self.exclude):
                continue
            # Read the file content
            content = content_handler.read_file(file)
            # Render the content
            content = engine.render_string(content, data)
            # Render the relative path
            relative_path = engine.render_string(os.path.join(path, relative), data)
            # Write the content to the new file
            content_handler.write_file(relative_path, content)
            rendered_files.append(relative_path)

        return rendered_files
    
    def validate_data(self, data: dict) -> bool:
        """
        Validate the given context data.

        :param data: The context data
        :return: True if the data is valid, False otherwise
        """
        for key, value in self.variables.items():
            if key not in data:
                return False
            if not isinstance(data[key], value):
                return False
        return True


class ITemplateRepository(ABC):

    @abstractmethod
    def get_template(self, name: str) -> Template:
        """
        Get the template with the given name.

        :param name: The name of the template
        :return: The template
        """
    
    @abstractmethod
    def list_templates(self) -> list[Template]:
        """
        List all the templates.

        :return: The list of templates
        """
