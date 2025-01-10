from typing import Callable, Protocol, Type


type PostProcessor = Callable[[dict], dict]


class ITemplate(Protocol):
    id: str
    name: str
    description: str
    variables: dict[str, Type]
    processors: list[PostProcessor]

    def list(self) -> list[tuple[str, Callable[[], str]]]:
        """
        :return: A list of tuples containing the file path and a callable that returns the file content.
        """
        pass