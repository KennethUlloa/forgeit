from forgeit.implementations.templates import FolderTemplate
from src.forgeit.implementations.processors import SnakeCase, PascalCase, KebabCase


TEMPLATES = {
    "flask.init": FolderTemplate(
        id="flask2",
        name="Flask api",
        description="Flask base project",
        variables={
            "project": {
                "name": str,
                "description": str,
                "author": str
            },
            "modules": list
        },
        processors=[
            SnakeCase("project.name", "project.slug")
        ],
        path="./templates/flask/api",
        remove="./templates/flask/api/",
    ),
    "flask:mod": FolderTemplate(
        id="mod",
        name="Flask mvc module",
        description="Flask app module base",
        variables={
            "project": {
                "slug": str
            },
            "module":{
                "name": str,
                "plural": str
            }
        },
        processors=[
            SnakeCase("module.name", "module.slug"),
            KebabCase("module.plural", "module.plural_url"),
            SnakeCase("module.plural", "module.plural_slug"),
            PascalCase("module.name", "module.pascal_case")
        ],
        path="./templates/flask/module",
        remove="./templates/flask/module/"
    )
}
