import rich_click as click
from rich.console import Console
from sqlings.config import Config
from sqlings.helpers import copy_starter
from sqlings.state import AppState
from sqlings.ui.app import SqlingsApp


@click.group()
@click.pass_context
def sqlings(ctx: click.Context):
    """Welcome to SQLings, the best way to learn SQL"""
    console = Console()
    try:
        ctx.obj = Config()
    except:
        console.print_exception()
        raise click.Abort()


@sqlings.command()
@click.pass_obj
@click.argument("project_name")
def new(config: Config, project_name: str):
    """Create a new folder with all your exercises"""
    console = Console()

    path = config.cwd / project_name

    try:
        config.project_name = project_name
        copy_starter(project_path=path)
        console.print(f"Project {project_name} created successfully! 🐣", style="green")
    except:
        console.print_exception()


@sqlings.command
@click.pass_obj
def start(config: Config):
    """
    Start the application that analyses your SQLings progress

    This will work in the following way:
        - 1 thread that draws the UI
            - Takes events as inputs (from a queue) and redraws ui when such an event occur
        - 1 thread that monitors the filesystem
            - Emits events to a queue when filesystem has been updated
        - 1 thread that monitors for keypresses from the terminal
            - Emits events to a queue based on keypresses


    """

    console = Console()
    try:
        state = AppState(config)
    except:
        console.print_exception()
        exit(0)

    app = SqlingsApp(state, config)
    app.run()
