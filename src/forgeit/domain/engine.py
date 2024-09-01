from abc import ABC, abstractmethod


class ITemplateEngine(ABC):
    @abstractmethod
    def render_string(self, string: str, data: dict) -> str:
        """
        Render a template with the given context data.

        :param string: The template string
        :param data: The context data
        :return: The rendered template
        """
