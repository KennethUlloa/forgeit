from datetime import datetime
from typing import Callable


def read(filename):
    return open(filename, "r", encoding="utf-8")


def save(filename):
    return open(filename, "w", encoding="utf-8")


class ExceptionLogger:
    def __init__(self, log_file: str, logger: Callable):
        self.log_file = log_file
        self.logger = logger

    def __enter__(self):
        pass

    def __exit__(self, exc_type, exc_val, exc_tb, *_args, **_kwargs):
        if not exc_val:
            return True
        now = datetime.today().strftime("%d-%m-%Y")
        with open(f"{self.log_file}_{now}.log", "a", encoding="utf-8") as f:
            self.logger(exc_type, exc_val, exc_tb)
            f.write(f"\n\n{datetime.now()}\n{exc_val}\n")

        return True
