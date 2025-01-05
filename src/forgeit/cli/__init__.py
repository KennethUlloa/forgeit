import json
import os
import rich
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from typer import Typer, Argument, Option
from .menu import IndexMenu
from .variables import load_variables
from ..values import ASCII, VERSION
from ..base import ITemplate, render
from ..settings import Setting


def format_template(template: ITemplate) -> str:
    return template.name


def observer(file, event):
    if event == "success":
        rich.print(f"[green]{file}[/green] created")
    if event == "fail":
        rich.print(f"[red]{file}[/red] failed")


def create_cli():
    cli = Typer(name="Forge it", help="A simple project generator")
    Setting.load_global()
    config_file_path = os.path.join(os.getcwd(), "forge_settings.py")
    if os.path.exists(config_file_path):
        Setting.load_from_file(config_file_path)

    @cli.command(name="t", hidden=True)
    @cli.command(
        name="template",
        help="Render a template",
    )
    def template_(
        template: str = Argument(None, help="The template name to use"),
        vars: str = Option(None, help="Use the variable file to set the template"),
        save_vars: bool = Option(False, help="Save variables to a file"),
    ):
        selected_template = None
        if not template:
            templates = list(Setting.TEMPLATES.values())
            menu = IndexMenu(templates, formatter=format_template, prefix=" * ")
            selected_template = menu.show("[bold]Select a template[/bold]")

        else:
            selected_template = Setting.TEMPLATES.get(template)

        if not selected_template:
            rich.print("[red]Template not found[/red]")
            return

        data = {}
        if vars and os.path.exists(vars):
            with open(vars, "r", encoding="utf-8") as f:
                data = json.loads(f.read())

        data.update(
            load_variables(
                "Enter the data:",
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
            Setting.ENGINE,
            path,
            Setting.ENCODING,
            observer,
        )

        if save_vars:
            with open(vars, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4))

        if len(failed) == 0:
            rich.print("[bold]Template rendered successfully[/bold]")
        else:
            if len(succeded) > 0:
                rich.print("[bold]Template rendered with errors[/bold]")
            else:
                rich.print("[bold]Template rendering failed[/bold]")

    @cli.command(name="ls", hidden=True)
    @cli.command(name="list", help="List the available templates")
    def list_():
        table = Table(title="Available templates")
        table.add_column("ID", justify="right", style="cyan")
        table.add_column("Name")
        table.add_column("Description")

        for template in Setting.TEMPLATES.values():
            table.add_row(template.id, template.name, template.description)
        
        Console().print(table)

    @cli.command(name="v", hidden=True)
    @cli.command(help="Show the tool's version")
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
