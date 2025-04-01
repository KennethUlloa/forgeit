import json
import rich
import os
from dataclasses import asdict
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt
from typer import Typer, Argument
from .template import render_template
from .db import open_db
from .meta import VERSION, ASCII
from .variables import Registry
from . import env


app = Typer(name="Forge it", help="A simple project generator")
env.init()


@app.command(help="Render a template's files given a name")
def init(
    template_name: str = Argument(None, help="The template name to use"),
    variables_file: str = Argument(None, help="JSON File with the needed variables"),
):
    with open_db() as db:
        template = db.get_template(template_name)

    if not template:
        rich.print(f"[yellow]Template '{template_name}' not found[/yellow]")
        return

    variables = {}
    if variables_file and os.path.exists(variables_file):
        with open(variables_file, "r", encoding="utf-8") as f:
            variables = json.load(f)
    else:
        variables = {
            name: Registry.get(value["type"])(**value)
            for name, value in template.variables.items()
        }

    root = Prompt.ask("Root path", default=".", show_default=True)

    ctx = env.create_context(root)
    variables.update({"_ctx": asdict(ctx)})

    for rendered_file in track(render_template(template, ctx, variables)):
        rich.print(f":white_check_mark: [green]{rendered_file}[/green]")


@app.command(
    help="Render a template's fragment using stored context ('.forge.json' file)"
)
def new(
    name: str = Argument(
        None, help="The subtemplate name (requires a parent template)"
    ),
):
    # TODO: reimplement subtemplates
    pass


@app.command(help="Install a template description from a file path")
def install(
    path: str = Argument(
        None, help="Real path for the file containing the template description"
    ),
):
    # TODO: reimplement template saving
    template = json.load(open(path, "r", encoding="utf-8"))
    with open_db() as db:
        db.save_template(template["name"], os.path.realpath(path))

    rich.print(f"[green]Template {template['name']} installed successfully![/green]")


@app.command(name="list", help="List all the available templates")
def list_all():
    # TODO: reimplement template listing
    with open_db() as db:
        data, columns = db.get_all_templates()

    table = Table(title="Installed templates")

    for col in columns:
        table.add_column(col)

    for row in data:
        rendered = [*row]
        active = row[-1]
        rendered[-1] = "active" if active else "inactive"
        table.add_row(*[r if active else f"[red]{r}[/red]" for r in rendered])

    rich.print(table)


@app.command(help="Display current version of the tool")
def version():
    prompt = f"""
[green]{ASCII}[/green]
Forgeit
Version [cyan]{VERSION}[/cyan]
"""
    rich.print(prompt)


@app.command(help="Information about")
def info():
    rich.print(f"[cyan]Application path[/cyan] {env.APP_DIR}")

if __name__ == "__main__":
    app()
