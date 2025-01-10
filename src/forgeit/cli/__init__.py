import json
import os
import pathlib
import rich
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from typer import Typer, Argument, Option
from .menu import IndexMenu
from .variables import load_variables
from ..values import ASCII, VERSION
from ..rendering import ITemplate, render
from ..config import config, load_object
from ..utils.serialization import load_binary, load_json, save_binary


def format_template(template: ITemplate) -> str:
    return template.name


def observer(file, event):
    if event == "success":
        rich.print(f"[green]{file}[/green] created")
    if event == "fail":
        rich.print(f"[red]{file}[/red] failed")


def load_config(read_cache=True, store_cache=True):
    cwd = os.getcwd()
    cache_path = os.path.join(cwd, "forge.cache")
    config
    if read_cache and os.path.exists(cache_path):
        try:
            return load_object(load_binary(cache_path))
        except Exception:
            pass
    global_config_path = os.path.join(
        pathlib.Path.home(), ".forgeit", "forge.config.json"
    )
    if os.path.exists(global_config_path):
        try:
            load_object(load_json(global_config_path))
        except Exception:
            pass

    local_config_path = os.path.join(cwd, "forge.config.json")
    if os.path.exists(local_config_path):
        load_object(load_json(local_config_path))

    if store_cache:
        save_binary(config, "forge.cache")


def create_cli():
    cli = Typer(name="Forge it", help="A simple project generator")

    @cli.command(name="t", hidden=True)
    @cli.command(
        name="template",
        help="(t) Render a template",
    )
    def template_(
        template: str = Argument(None, help="The template name to use"),
        file: str = Option(None, help="Load variables from a json file template"),
        save: bool = Option(False, help="Save variables to a file as json"),
        cache: bool = Option(True, help="Use the cache from the working directory"),
    ):
        load_config(cache)

        selected_template = None
        if not template:
            templates = list(config.TEMPLATES.values())
            menu = IndexMenu(templates, formatter=format_template, prefix=" * ")
            selected_template = menu.show("[bold]Select a template[/bold]")

        else:
            selected_template = config.TEMPLATES.get(template)

        if not selected_template:
            rich.print("[red]Template not found[/red]")
            return

        data = {}
        if file and os.path.exists(file):
            with open(file, "r", encoding="utf-8") as f:
                data = json.loads(f.read())

        data.update(
            load_variables(
                {
                    key: type_
                    for key, type_ in selected_template.variables.items()
                    if key not in data
                },
            )
        )

        path = Prompt.ask(
            "Enter the template's root path", default=".", show_default=True
        )

        succeded, failed = render(
            selected_template,
            data,
            config.ENGINE,
            path,
            config.ENCODING,
            observer,
        )

        if save:
            file = file or Prompt.ask(
                "Enter the name of the file to store the variables",
                default="forge.variables.json",
            )
            if not file:
                raise ValueError("No filename provided")
            with open(file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4))

        if len(failed) == 0:
            rich.print("[bold]Template rendered successfully[/bold]")
        else:
            if len(succeded) > 0:
                rich.print("[bold]Template rendered with errors[/bold]")
            else:
                rich.print("[bold]Template rendering failed[/bold]")

    @cli.command(name="ls", hidden=True)
    @cli.command(name="list", help="(ls) List the available templates")
    def list_(
        cache: bool = Option(True, help="Use the cache from the working directory"),
    ):
        load_config(cache)

        table = Table(title="Available templates")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name")
        table.add_column("Description")

        for key, template in config.TEMPLATES.items():
            table.add_row(key, template.name, template.description)

        Console().print(table)

    @cli.command(name="v", hidden=True)
    @cli.command(help="(v) Show the tool's version")
    def version():
        rich.print(
            f"[bold][blue]{ASCII}[/blue][/bold]\n[bold]ForgeIt[/bold]\nversion: [green]{VERSION}[/green]\nauthor: [green]Kenneth Ulloa[/green]\n"
        )

    return cli


def run():
    """
    Run the CLI application
    """
    cli = create_cli()
    cli()
