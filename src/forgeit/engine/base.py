from typing import Protocol


class ITemplateEngine(Protocol):
    def render(self, content: str, data: dict) -> str:
        """
        Render the template with the given context data.

        :param content: The template content
        :param data: The context data
        :return: The rendered template
        """
        pass
