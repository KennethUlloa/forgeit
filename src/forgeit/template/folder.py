import os
import glob
from typing import Callable, Type
from .base import ITemplate, PostProcessor


class FolderTemplate(ITemplate):
    def __init__(
        self,
        id: str,
        name: str,
        description: str,
        path: str,
        variables: dict[str, Type] = {},
        processors: list[PostProcessor] = [],
        pattern: str = None,
        remove: str = "",
        encoding: str = "utf-8",
    ):
        self.id = id
        self.name = name
        self.description = description
        self.variables = variables
        self.processors = processors
        self.path = path
        self.pattern = pattern
        self.encoding = encoding
        self.remove = remove

    def list(self) -> list[tuple[str, Callable[[], str]]]:
        if not os.path.isdir(self.path):
            raise ValueError(
                f"The provided path '{self.path}' is not a valid directory."
            )

        def create_callable(file_path: str):
            normalized = file_path.replace("\\", "/")
            removed_path = normalized.replace(self.remove, "")

            def content():
                with open(file_path, "r", encoding=self.encoding) as file:
                    return file.read()

            return removed_path, content

        if not self.pattern:
            all_files = []
            for root, _, files in os.walk(self.path):
                for file in files:
                    all_files.append(create_callable(os.path.join(root, file)))
            return all_files

        pattern = os.path.join(self.path, self.pattern)
        
        return [
            create_callable(f)
            for f in glob.glob(pattern, recursive=True)
            if os.path.isfile(f)
        ]
