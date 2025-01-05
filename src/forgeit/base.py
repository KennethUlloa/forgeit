import os
from typing import Protocol, Callable, Type, Union


type TypeCallable = Union[Callable[[str], Type] | Type]
type PostProcessor = Callable[[dict], dict]
type Observer = Callable[[str, str], None]


class ITemplate(Protocol):
    id: str
    name: str
    description: str
    variables: dict[str, TypeCallable]
    processors: list[PostProcessor]

    def list(self) -> list[tuple[str, Callable[[], str]]]:
        """
        :return: A list of tuples containing the file path and a callable that returns the file content.
        """
        pass


class ITemplateEngine(Protocol):
    def render(self, content: str, data: dict) -> str:
        """
        Render the template with the given context data.

        :param content: The template content
        :param data: The context data
        :return: The rendered template
        """
        pass


def render(
    template: ITemplate,
    data: dict[str, str],
    engine: ITemplateEngine,
    relative_path: str = ".",
    encoding: str = "utf-8",
    observer: Observer = None 
) -> tuple[list[str], tuple[str, Exception]]:
    """
    Render the template with the given context data.

    :param template: The template to be rendered
    :param data: The context data
    :param engine: The template engine
    :param relative_path: Path to append to all templates
    :param encoding: Encoding to use when on read/write operations
    :return: tuple containing the list of succeded files, tuple containing the failed files and the exception
    """
    processed_data = data.copy()

    # Apply variables type casting
    for key, type_ in template.variables.items():
        if key in data:
            processed_data[key] = type_(data[key])

    # Process the data with the processors

    for processor in template.processors:
        processed_data = processor(processed_data)

    succeded = []
    failed = []
    # Render the template
    for file_path, content in template.list():
        try:
            rendered_file_path = engine.render(file_path, processed_data)
            rendered_content = engine.render(content(), processed_data)
            # Save the rendered content
            os.makedirs(
                os.path.join(relative_path, os.path.dirname(rendered_file_path)),
                exist_ok=True,
            )  # Create the directory if it does not exist
            with open(
                os.path.join(relative_path, rendered_file_path), "w", encoding=encoding
            ) as file:
                file.write(rendered_content)

            succeded.append(rendered_file_path)
            if observer:
                observer(rendered_file_path, "success")
        except Exception as e:
            failed.append((file_path, e))
            if observer:
                observer(rendered_file_path, "fail")

    return succeded, failed
