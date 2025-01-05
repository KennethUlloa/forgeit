from src.forgeit.implementations.file_tree_template import FileTreeTemplate
from src.forgeit.implementations.processors import SnakeCaseProcessor


TEMPLATES = {
    "flask": FileTreeTemplate(
        id="flask",
        name="Flask api",
        description="A template that renders a file tree",
        variables={
            "project_name": str,
            "project_description": str,
            "project_author": str,
        },
        processors=[
            SnakeCaseProcessor("project_name", "project_slug")
        ],
        path=".",
        pattern="templates/flask/api/**",
        remove="templates/flask/api/",
        encoding="utf-8",
    )
}
