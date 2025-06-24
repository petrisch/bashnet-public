import click
from .semantic_net import SemanticNet
from .node import Node
from .edge import Edge

# Dummy data for testing (will be replaced by JSON import later)
def build_test_net():
    net = SemanticNet()
    net.add_node(Node("ls", "ls", "command", description="List directory contents"))
    net.add_node(Node("-l", "-l", "option", description="use a long listing format"))
    net.add_edge(Edge("ls", "-l", "uses"))
    return net

@click.command()
@click.argument("term")
@click.option("--simple", is_flag=True, help="Perform a simple search without following relations.")
def search(term, simple):
    """Search for a term in the semantic network."""
    net = build_test_net()
    result = net.get_node(term)

    if not result:
        click.secho(f"Error: Term '{term}' not found.", fg="red")
        return

    click.secho(f"\nTerm found: {result['label']} ({result['type']})", fg="green")
    if not simple:
        neighbors = net.get_neighbors(term)
        if neighbors:
            click.echo("Related concepts:")
            for nid in neighbors:
                info = net.get_node(nid)
                click.echo(f"- {info['label']} ({info['type']})")

@click.command()
def cli():
    """Start the CLI search application. Exit with CTRL+C or 'exit'."""
    click.secho("Welcome to the Bashnet search. Enter terms like 'ls --simple'", fg="cyan")
    while True:
        try:
            cmd = input("Enter search term: ").strip()
            if cmd.lower() in ["exit", "quit"]:
                break
            parts = cmd.split()
            term = parts[0] if parts else ""
            simple = "--simple" in parts
            search.main(args=[term] + (["--simple"] if simple else []), standalone_mode=False)
        except KeyboardInterrupt:
            click.secho("\nTerminated with CTRL+C", fg="yellow")
            break

if __name__ == "__main__":
    cli()
