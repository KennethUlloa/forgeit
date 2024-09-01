import os
import fnmatch

def list_files(directory: str, exclude_extensions: list[str] = []) -> list[str]:
    found_files: list[str] = []
    extensions = tuple(exclude_extensions)
    for root, dirs, files in os.walk(directory):
        for file in files:
            if not file.endswith(extensions):
                found_files.append(os.path.join(root, file))
    return found_files

def remove_base(file: str, base: str):
    return file.replace(f"{base}", "").removeprefix("\\").removeprefix("/")

def listdirs(directory: str) -> list[str]:
    return [d for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]


def match_pattern(file: str, patterns: list[str]) -> bool:
    for pattern in patterns:
        if fnmatch.fnmatch(file, pattern):
            return True
    return False