# Setup environment to get/store template metadata
import os
import sys
from datetime import datetime
from .model import Context
global APP_DIR

APP_NAME = 'forgeit'
APP_DIR = '.'
CURRENT_TEMPLATE = f".{APP_NAME}.json"
CWD = os.getcwd().replace("\\\\", "/").replace("\\", "/")

def init():
    global APP_DIR
    match sys.platform:
        case 'win32':
            APP_DIR = os.path.join(os.getenv('APPDATA'), APP_NAME)
        case 'darwin':
            APP_DIR = os.path.join(os.path.expanduser('~/Library/Application Support'), APP_NAME)
        case _:
            APP_DIR = os.path.join(os.path.expanduser("~/.config"), APP_NAME)
    
    APP_DIR = APP_DIR.replace("\\\\", "/").replace("\\", "/")

    os.makedirs(APP_DIR, exist_ok=True)


def create_context(root: str) -> Context:
    return Context(
        root=root,
        cwd=CWD,
        app_name=APP_NAME
    )
