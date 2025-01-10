import os
from typing import Callable
from .template import ITemplate
from .engine import ITemplateEngine

type Observer = Callable[[str, str], None]


def render(
    template: ITemplate,
    data: dict[str, str],
    engine: ITemplateEngine,
    relative_path: str = ".",
    encoding: str = "utf-8",
    observer: Observer = None,
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
    print(relative_path)
    processed_data = data.copy()

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
            full_file_path = os.path.join(relative_path, rendered_file_path)
            print(full_file_path)
            with open(full_file_path, "w", encoding=encoding) as file:
                file.write(rendered_content)

            succeded.append(full_file_path)
            if observer:
                observer(full_file_path, "success")
        except Exception as e:
            print(e)
            failed.append((file_path, e))
            if observer:
                observer(file_path, "fail")

    return succeded, failed
