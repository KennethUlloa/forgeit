# Setup environment to get/store template metadata
import os
import sys
from .model import Context

global APP_DIR

APP_NAME = "forgeit"
APP_DIR = "."
CWD = os.getcwd()
CACHE_FILE = os.path.join(CWD, f".{APP_NAME}.json")


def init():
    global APP_DIR
    match sys.platform:
        case "win32":
            APP_DIR = os.path.join(os.getenv("APPDATA"), APP_NAME)
        case "darwin":
            APP_DIR = os.path.join(
                os.path.expanduser("~/Library/Application Support"), APP_NAME
            )
        case _:
            APP_DIR = os.path.join(os.path.expanduser("~/.config"), APP_NAME)

    APP_DIR = os.path.normpath(APP_DIR)
    os.makedirs(APP_DIR, exist_ok=True)


def create_context(root: str) -> Context:
    return Context(root=root, cwd=CWD, app_name=APP_NAME)
