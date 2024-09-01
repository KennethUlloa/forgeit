import json
import os
import rich
from typing import Callable
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt
from typer import Typer, Argument, Option
from forgeit.application import Forge
from forgeit.domain.template import Template
from forgeit.config import default, VERSION
from .menu import IndexMenu
from .variables import load_variables


ASCII_ART = \
r"""
  ______                   _____ _   
 |  ____|                 |_   _| |  
 | |__ ___  _ __ __ _  ___  | | | |_ 
 |  __/ _ \| '__/ _` |/ _ \ | | | __|
 | | | (_) | | | (_| |  __/_| |_| |_ 
 |_|  \___/|_|  \__, |\___|_____|\__|
                 __/ |               
                |___/
"""


def format_template(template: Template) -> str:
    return template.description


def create_cli(pyvite_factory: Callable[[], Forge]=default):
    cli = Typer(name="Forge it", help="A simple project generator")
    app = pyvite_factory()

    @cli.command(help="Create a new project based on a template")
    def project(
        template: str = Argument(None, help="The template name to use"),
        var_file: str = Option("forge.vars.json", help="Use the configuration file to set the template"),
        use_vars: bool = Option(True, help="Use variables from a file"),
        save_vars: bool = Option(False, help="Save variables to a file"),
        ):
        selected_template = None
        if not template:
            templates = app.templates_list()
            menu = IndexMenu(templates, formatter=format_template, prefix=" * ")
            selected_template = menu.show("[bold]Select a template[/bold]")
        
        else:
            selected_template = app.get_template(template)

        if not selected_template:
            rich.print("[red]Template not found[/red]")
            return
        
        data = {}
        if os.path.exists(var_file) and use_vars:
            with open(var_file, "r", encoding="utf-8") as f:
                data = json.loads(f.read())
        
        data.update(
            load_variables(
            "Enter the following data:", 
            {key: type_ for key, type_ in selected_template.variables.items() if key not in data}))

        path = Prompt.ask("Enter the path to save the project", default=".", show_default=True)

        result = []

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            progress.add_task("Creating project...", None)
            result = app.render_template(selected_template, path, data)

        if save_vars:
            with open(var_file, "w", encoding="utf-8") as f:
                f.write(json.dumps(data, indent=4))

        for file in result:
            rich.print(f"[green]{file}[/green] created")

        rich.print("[bold]Project created successfully[/bold]")
    

    @cli.command(name="list", help="List the available templates")
    def list_templates():
        rich.print("[bold]Available templates:[/bold]")
        templates = app.templates_dict()
        for template in templates.values():
            rich.print(f"[green]{template.name}[/green]: {template.description}")

    @cli.command(help="Show the version of the application")
    def version():
        rich.print(f"[bold][blue]{ASCII_ART}[/blue][/bold]\nForgeIt\nversion: [green]{VERSION}[/green]")

    return cli

def run():
    """
    Run the CLI application
    """
    cli = create_cli()
    cli()
