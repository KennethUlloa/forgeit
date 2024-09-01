import os
from ..domain.content import IContentHandler


class FSContentHandler(IContentHandler):
    def list_files(self, folder: str) -> list[tuple[str, str]]:
        found_files: list[str] = []
        for root, dirs, files in os.walk(folder):
            for file in files:
                found_files.append(os.path.join(root, file))
        
        return [(file, self.relative_path(file, folder)) for file in found_files]

    def read_file(self, file: str) -> str:
        with open(file, "r") as f:
            return f.read()

    def write_file(self, file: str, content: str):
        os.makedirs(os.path.dirname(file), exist_ok=True)
        with open(file, "w", encoding="utf-8") as f:
            f.write(content)

    def relative_path(self, file: str, folder: str) -> str:
        return file.replace(folder, "").removeprefix("\\").removeprefix("/")
