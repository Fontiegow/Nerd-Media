import click
import crud


@click.group()
@click.version_option(version="0.1.0")
@click.pass_context
def cli() -> None:
    """Entry point for the Nerdial CLI."""
    print("Welcome to the Nerdial CLI!")

cli.add_command(crud.hello)
cli.add_command(crud.repeat)
cli.add_command(crud.status)