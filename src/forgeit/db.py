import sqlite3
import os
import json
from dataclasses import asdict
from . import env, model, utils


def serialize(template: model.Template) -> str:
    dict_data = asdict(template)

    if "id" in dict_data:
        dict_data.pop("id")

    return json.dumps(dict_data)


def deserialize(json_str: str) -> model.Template:
    json_data = json.loads(json_str)
    return model.Template(**json_data)


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
                label TEXT NOT NULL,
                description TEXT NOT NULL,
                active INTEGER NOT NULL DEFAULT 1,
                json TEXT NOT NULL
            )
        """)
        self.__connection.commit()
        return self.__connection

    def get_template(self, template_name: str):
        cursor = self.__connection.cursor()
        res = cursor.execute(
            "SELECT id, json FROM template WHERE name = ? AND active = 1 LIMIT 1",
            (template_name,),
        )

        res = res.fetchone()

        if not res:
            return None

        _id, _json = res
        template = deserialize(_json)
        template.id = _id
        return template

    def save_template(self, template: model.Template):
        if not template:
            raise ValueError("Can't store empty objects")

        data = (
            template.name,  # name
            template.label,  # label
            template.description,  # description
            serialize(template),  # json
            True,  # active
        )

        cursor = self.__connection.cursor()
        cursor.execute(
            "INSERT INTO template(name, label, description, json, active) VALUES (?,?,?,?,?)",
            data,
        )
        self.__connection.commit()

    def get_all_templates_data(self) -> list[model.TemplateData]:
        cursor = self.__connection.cursor()
        res = cursor.execute("SELECT id, name, description, active FROM template")
        return [
            model.TemplateData(
                id=row[0], name=row[1], description=row[2], active=bool(row[3])
            )
            for row in res
        ]

    def __enter__(self):
        self.__load_connection()
        return self

    def __exit__(self, *_args, **_kwargs):
        self.__connection.close()
        return False


def opendb():
    return __DatabaseContext()
