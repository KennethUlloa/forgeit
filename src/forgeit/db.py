import sqlite3
import os
import json
from . import env, model


class __DatabaseContext:
    def __init__(self):
        self.__connection_string = os.path.join(env.APP_DIR, "forgeit.db")
        self.__connection = None

    def __load_connection(self):
        self.__connection = sqlite3.connect(self.__connection_string)
        cursor = self.__connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS template (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                path TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1  
            )
        """)
        self.__connection.commit()
        return self.__connection

    def get_template(self, template_name: str):
        cursor = self.__connection.cursor()
        res = cursor.execute(
            "SELECT id, path FROM template WHERE name = ? AND active = 1 LIMIT 1", (template_name,)
        )

        res = res.fetchone()

        if not res:
            return None
        
        _id, path = res
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
            data["path"] = path
            data["id"] = _id
            return model.Template(**data)


    def save_template(self, name: str, path: str):
        if not os.path.exists(path):
            raise Exception(f"Invalid path {path}")

        data = (name, path, True)
        cursor = self.__connection.cursor()
        cursor.execute("INSERT INTO template(name, path, active) VALUES (?,?,?)", data)
        self.__connection.commit()
    
    def get_all_templates(self):
        cursor = self.__connection.cursor()
        res = cursor.execute("SELECT name, path, active FROM template")
        return res.fetchall(), ["Name", "Path", "Active"]

    def __enter__(self):
        self.__load_connection()
        return self

    def __exit__(self, *_args, **_kwargs):
        self.__connection.close()
        return False


def open_db():
    return __DatabaseContext()
