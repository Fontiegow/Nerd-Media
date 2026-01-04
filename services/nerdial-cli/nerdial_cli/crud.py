import click

@click.command()
@click.option('--name', prompt='Your name', help='The person to greet.')
def hello(name):
    """Simple program that greets NAME for a total of COUNT times."""
    click.echo(f"Hello, {name}!")

@click.command()
@click.argument('count', default=1, type=int)
def repeat(count):
    """Simple program that repeats a greeting COUNT times."""
    for _ in range(count):
        click.echo("Hello!")

# status command to check if the service is running
@click.command()
def status():
    """Check if the service is running."""
    click.echo("Service is running.")

