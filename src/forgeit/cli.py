import json
import shutil
import rich
import os
import zipfile
import jsonschema
from dataclasses import asdict
from rich.table import Table
from rich.progress import track
from rich.prompt import Prompt
from typer import Typer, Argument, Option
from .utils import read, save, ExceptionLogger
from .model import Template, Cache, SubTemplate, Context
from .template import TemplateRenderer, template_path
from .db import opendb
from .meta import VERSION, ASCII
from .input import Registry
from .schemas import validate_template
from . import env


app = Typer(
    name="Forge it", help="A simple project generator", pretty_exceptions_enable=False
)
env.init()


def error_logger(exc_type, exc_val, exc_tb):
    rich.print(f"[red]{exc_val}[/red]")


def logger():
    return ExceptionLogger("forgeit-crash", error_logger)


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
    cache_path = os.path.join(os.getcwd(), env.CACHE_FILE)
    if not os.path.exists(cache_path):
        return None

    with read(cache_path) as f:
        return Cache(**json.load(f))


def save_cache(cache: Cache, root: str = None):
    cache_dict = asdict(cache)
    if "_ctx" in cache_dict["variables"]:
        cache_dict["variables"].pop("_ctx")

    cache_path = os.path.join(root or os.getcwd(), env.CACHE_FILE)
    with save(cache_path) as f:
        json.dump(cache_dict, f)


@app.command(help="Render a template's files given a name")
def init(
    template_name: str = Argument(None, help="The template name to use"),
    variables_file: str = Argument(None, help="JSON File with the required variables"),
):
    with logger():
        with opendb() as db:
            template = db.get_template(template_name)

        if not template:
            rich.print(f"[yellow]Template '{template_name}' not found[/yellow]")
            return

        root = Prompt.ask("Root path", default=".", show_default=True)
        ctx = env.create_context(root)
        variables = get_variables(template.variables, ctx, variables_file)

        renderer = TemplateRenderer(template, ctx, variables)
        for callback in renderer.render_callbacks(root):
            rich.print(f":white_check_mark: [green]{callback()}[/green]")

        save_cache(Cache(template=template_name, variables=variables), root)


@app.command(
    help="Render a template's fragment using stored context ('.forge.json' file)"
)
def new(
    name: str = Argument(
        None, help="The subtemplate name (requires a parent template)"
    ),
    variables_file: str = Argument(None, help="JSON File with the required variables"),
):
    with logger():
        cache = load_cache()

        if not cache:
            error("No parent template was found")
            return

        with opendb() as db:
            parent_template = db.get_template(cache.template)

        if not parent_template:
            error(f"Malformed cache file: {cache.template} is not a valid template")
            return

        if not name:
            rich.print(f"You must specify a subtemplate name.")
            if len(parent_template.subtemplates) > 0:
                rich.print("Available subtemplates:")
            for name, data in parent_template.subtemplates.items():
                rich.print(f"* [green]{name}[/green] {data['description']}")
            return

        if name not in parent_template.subtemplates:
            error(f"Subtemplate {name} wasn't found")
            return

        template = SubTemplate(
            **parent_template.subtemplates[name], parent_name=parent_template.name
        )

        ctx = env.create_context(".")
        variables = cache.variables
        variables.update(get_variables(template.variables, ctx, variables_file))
        renderer = TemplateRenderer(template, ctx, variables)
        for callback in renderer.render_callbacks("."):
            rich.print(f":white_check_mark: [green]{callback()}[/green]")


@app.command(help="Install a template description from a file path")
def install(
    path: str = Argument(
        None, help="Real path for the file containing the template description (.zip)"
    ),
    update: bool = Option(False, help="Update an existing template"),
):
    with logger():
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

                with opendb() as db:
                    rich.print("[cyan]Saving template...[/cyan]")
                    db.save_template(template, update)

                files = [f for f in zip.infolist() if f.filename != "template.json"]

                t_path = template_path(template)

                rich.print("[cyan]Saving template files...[/cyan]")
                for f in track(files, description="Extracting files..."):
                    zip.extract(f, t_path)

            rich.print(
                "Template installed successfully. Run 'forgeit list' to verify it"
            )
            return

        if os.path.isdir(path):
            template_file_path = os.path.join(path, "template.json")

            if not os.path.exists(template_file_path):
                error("Template description file not found")
                return

            with open(os.path.join(path, "template.json"), "r") as f:
                template_data = json.load(f)
                validate_template(template_data)
                template = Template(**template_data)

                with opendb() as db:
                    db.save_template(template, update)

            rich.print("[cyan]Saving template files...[/cyan]")
            template_files_path = template_path(template)
            for root, dirs, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    relative_path = os.path.relpath(root, path)
                    destination_path = os.path.join(template_files_path, relative_path)
                    os.makedirs(destination_path, exist_ok=True)
                    shutil.copy2(file_path, destination_path)

            rich.print(
                "Template installed successfully. Run 'forgeit list' to verify it"
            )
            return


@app.command(help="Validate a template description")
def validate(
    path: str = Argument(
        None, help="Real path for the file containing the template description (.json)"
    ),
):
    with logger():
        try:
            if not path or not os.path.exists(path):
                error("Path doesn't exists")
                return

            if not path.endswith(".json"):
                error("Invalid extension, expected: json")
                return

            with open(path, "r") as f:
                template = json.load(f)

            validate_template(template)
        except jsonschema.ValidationError as err:
            error(str(err))


@app.command(name="list", help="List all the available templates")
def list_all():
    with logger():
        with opendb() as db:
            templates = db.get_all_templates_data()

        if len(templates) == 0:
            rich.print(
                "No templates available. To install a template run 'forgeit install <template file/directory>' then run again this command to verify the installation"
            )
            return

        table = Table(title="Installed templates")
        columns = ["Name", "Description", "Status"]
        for col in columns:
            table.add_column(col)

        for template in templates:
            active = "Active" if template.active else f"[red]Inactive[/red]"
            table.add_row(template.name, template.description, active)

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
    with logger():
        from importlib.resources import files

        source = files("forgeit").joinpath("data/flask-api.zip")
        shutil.copy(source, "example.zip")
        rich.print(
            "[green]Example created successfully.[/green] Run 'forgeit install example.zip' to install the template"
        )


@app.command(help="Delete an existing template")
def delete(template_name: str = Argument(help="The template name to be deleted")):
    with logger():
        with opendb() as db:
            if db.delete_template(template_name):
                rich.print(
                    "Template successfully deleted. Run 'forgeit list' to verify it"
                )
            else:
                rich.print("Template not deleted. Check the template name")


if __name__ == "__main__":
    app()
