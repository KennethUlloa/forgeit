from abc import ABC, abstractmethod


class IContentHandler(ABC):
    @abstractmethod
    def list_files(self, path: str) -> list[tuple[str, str]]:
        """
        List the files in the given folder.

        :param path: The path to list
        :return: The list of files in the path where each file is a tuple containing the full path and the path relative to the path
        """
    
    @abstractmethod
    def read_file(self, file: str) -> str:
        """
        Read the contents of the given file.

        :param folder: The folder containing the file
        :param file: The file to read
        :return: The file contents
        """

    @abstractmethod
    def write_file(self, file: str, content: str):
        """
        Write the given content to the given file.

        :param folder: The folder containing the file
        :param file: The file to write
        :param content: The content to write
        """
