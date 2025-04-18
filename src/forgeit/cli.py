import json
import rich
import os
import zipfile
from dataclasses import asdict
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt
from typer import Typer, Argument, Option
from .utils import read, save
from .model import Template, Cache, SubTemplate, Context
from .template import TemplateRenderer, template_path
from .db import opendb
from .meta import VERSION, ASCII
from .input import Registry
from .schemas import validate_template
from . import env


app = Typer(name="Forge it", help="A simple project generator")
env.init()


def error(*messages: str):
    rich.print("[red]" + " ".join(messages) + "[/red]")


def get_variables(variables_schema: dict, ctx: Context, variables_file: str = None):
    variables = {}
    if variables_file and os.path.exists(variables_file):
        with read(variables_file) as f:
            variables = json.load(f)
    else:
        variables = {
            name: Registry.get(value["type"])(**value)
            for name, value in variables_schema.items()
        }

    variables.update({"_ctx": asdict(ctx)})

    return variables


def load_cache():
    if not os.path.exists(env.CACHE_FILE):
        return None

    with read(env.CACHE_FILE) as f:
        return Cache(**json.load(f))


def save_cache(cache: Cache):
    cache_dict = asdict(cache)
    if "_ctx" in cache_dict["variables"]:
        cache_dict["variables"].pop("_ctx")

    with save(env.CACHE_FILE) as f:
        json.dump(cache_dict, f)


@app.command(help="Render a template's files given a name")
def init(
    template_name: str = Argument(None, help="The template name to use"),
    variables_file: str = Argument(None, help="JSON File with the required variables"),
):
    with opendb() as db:
        template = db.get_template(template_name)

    if not template:
        rich.print(f"[yellow]Template '{template_name}' not found[/yellow]")
        return

    root = Prompt.ask("Root path", default=".", show_default=True)
    ctx = env.create_context(root)
    variables = get_variables(template.variables, ctx, variables_file)

    save_cache(Cache(template=template_name, variables=variables, root=root))

    renderer = TemplateRenderer(template, ctx, variables)
    for callback in renderer.render_callbacks(root):
        rich.print(f":white_check_mark: [green]{callback()}[/green]")


@app.command(
    help="Render a template's fragment using stored context ('.forge.json' file)"
)
def new(
    name: str = Argument(
        None, help="The subtemplate name (requires a parent template)"
    ),
    variables_file: str = Argument(None, help="JSON File with the required variables"),
):
    cache = load_cache()

    if not cache:
        error("No parent template was found")
        return

    with opendb() as db:
        parent_template = db.get_template(cache.template)

    if not parent_template:
        error(f"Malformed cache file: {cache.template} is not a valid template")
        return

    if name not in parent_template.subtemplates:
        error(f"Subtemplate {name} wasn't found")
        return

    template = SubTemplate(
        **parent_template.subtemplates[name], parent_name=parent_template.name
    )

    ctx = env.create_context(cache.root)
    variables = cache.variables
    variables.update(get_variables(template.variables, ctx, variables_file))
    renderer = TemplateRenderer(template, ctx, variables)
    for callback in renderer.render_callbacks(cache.root):
        rich.print(f":white_check_mark: [green]{callback()}[/green]")


@app.command(help="Install a template description from a file path")
def install(
    path: str = Argument(
        None, help="Real path for the file containing the template description (.zip)"
    ),
):
    if not os.path.exists(path):
        error("Path doesn't exists")
        return

    if path.endswith(".zip"):
        with zipfile.ZipFile(path, "r") as zip:
            if "template.json" not in zip.namelist():
                raise Exception('"template.json" file missing in ZIP file')

            with zip.open("template.json", "r") as file:
                rich.print("[cyan]Validating template...[/cyan]")
                template_data = json.load(file)
                validate_template(template_data)
                template = Template(**template_data)

            files = [f for f in zip.infolist() if f.filename != "template.json"]

            t_path = template_path(template)
            
            rich.print("[cyan]Saving template files...[/cyan]")
            for f in track(files, description="Extracting files..."):
                zip.extract(f, t_path)

            with opendb() as db:
                rich.print("[cyan]Saving template...[/cyan]")
                db.save_template(template)

        rich.print("Template installed successfully")
        return

    rich.print("Invalid extension, expected: zip")


@app.command(help="Validate a template description")
def validate(
    path: str = Argument(
        None, help="Real path for the file containing the template description (.json)"
    ),
):
    if not path or not os.path.exists(path):
        error("Path doesn't exists")
        return

    if not path.endswith(".json"):
        error("Invalid extension, expected: json")
        return

    with open(path, "r") as f:
        template = json.load(f)

    validate_template(template)


@app.command(name="list", help="List all the available templates")
def list_all():
    with opendb() as db:
        templates = db.get_all_templates_data()

    table = Table(title="Installed templates")
    columns = ["ID", "Name", "Description", "Status"]
    for col in columns:
        table.add_column(col)

    for template in templates:
        active = "Active" if template.active else f"[red]Inactive[/red]"
        table.add_row(str(template.id), template.name, template.description, active)

    rich.print(table)


@app.command(help="Display current version of the tool")
def version(
    verbose: bool = Option(
        False, "--verbose", "-v", help="Display more information about the tool"
    ),
):
    if not verbose:
        prompt = VERSION
    else:
        prompt = f"""[green]{ASCII}[/green]
ForgeIt
Version [cyan]{VERSION}[/cyan]
"""
    rich.print(prompt)


@app.command(help="Create an example template")
def example():
    html_template = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Document</title>
</head>
<body>
    Name: {{ name }}, Email: {{ email }}
    <script src="script.js"></script>
</body>
</html>
"""

    javascript_template = """alert('Hello, {{ name }}!');"""

    css_template = """body {
    background-color: #f0f0f0;
    color: #333;
}"""
    example_template = {
        "label": "Example",
        "name": "example",
        "description": "Example template",
        "variables": {
            "name": {"type": "string", "label": "Name"},
            "email": {"type": "string", "label": "Email"},
        },
        "content": {
            "README.md": "content:# Example\n- Hello {{name}}\n- Email: {{email}}",
            "LICENSE": "content:MIT",
            "index.html": "template:index.html.j2",
            "style.css": "file:style.css",
            "script.js": "template:script.js.j2",
        },
    }

    with zipfile.ZipFile("example.zip", "w") as zip:
        with zip.open("template.json", "w") as file:
            text = json.dumps(example_template)
            file.write(text.encode("utf-8"))

        with zip.open("templates/index.html.j2", "w") as file:
            file.write(html_template.encode("utf-8"))

        with zip.open("files/style.css", "w") as file:
            file.write(css_template.encode("utf-8"))

        with zip.open("templates/script.js.j2", "w") as file:
            file.write(javascript_template.encode("utf-8"))

    rich.print("Example template created successfully")


if __name__ == "__main__":
    app()
