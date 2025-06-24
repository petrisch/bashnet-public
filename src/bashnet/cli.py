import click
from .cli_core import BashnetCLI

@click.group()
@click.pass_context
def cli(ctx):
    """Bashnet CLI entry point."""
    ctx.obj = BashnetCLI()

@cli.command()
@click.pass_obj
def import_data(cli: BashnetCLI):
    """Import JSON data and persist the knowledge network."""
    cli.import_data()

@cli.command()
@click.argument("term")
@click.option("--simple", is_flag=True, help="Perform a simple search without following relations.")
@click.pass_obj
def search(cli: BashnetCLI, term, simple):
    """Search for a term in the semantic network."""
    try:
        cli.load_knowledge_net()
    except FileNotFoundError as e:
        click.secho(str(e), fg="red")
        return
    cli.search(term, simple)
