import click
import webbrowser
from .cli_core import BashnetCLI
from .utils import print_node_info, print_deep_search_context


def print_help():
    click.secho("Welcome to Bashnet CLI – Your semantic Bash learning tool!\n", fg="cyan")
    click.echo("Available commands:")
    click.echo("    import                      => Load all JSON files and rebuild the semantic net")
    click.echo("    search <term>               => Deep search: context-aware with related information")
    click.echo("    search <term> --simple      => Simple search: exact node only")
    click.echo("    visualize                   => Generate and open an interactive HTML graph")
    click.echo("    help                        => Show this help again")
    click.echo("    exit                        => Exit the application")
    click.echo("Press Ctrl+C anytime to exit.\n")


def handle_search(cli: BashnetCLI, term: str, simple: bool):
    cli.load_knowledge_net()

    if simple:
        node = cli.simple_search(term)
        if node:
            print_node_info(node)
        else:
            click.secho(f"Term '{term}' not found.", fg="red")
    else:
        node, context = cli.deep_search(term)
        if node:
            print_node_info(node)
            print_deep_search_context(node, context)
        elif context.get("fallback"): 
            click.secho(f"Term '{term}' not found directly. Showing relevant matches:\n", fg="yellow")
            from .utils import print_context_fallback
            print_context_fallback(context)
        else:
            click.secho(f"Term '{term}' not found.", fg="red")



def main():
    cli = BashnetCLI()
    print_help()

    while True:
        try:
            user_input = input("bashnet> ").strip()
            if not user_input:
                continue
            if user_input.lower() == "exit":
                break

            args = user_input.split()
            cmd = args[0]

            if cmd == "import":
                cli.import_data()

            elif cmd == "search":
                if len(args) < 2:
                    click.secho("Error: Please provide a term to search.", fg="red")
                    continue
                term = args[1]
                simple = "--simple" in args
                handle_search(cli, term, simple)
            
            elif cmd == "visualize":
                try:
                    cli.load_knowledge_net()
                    html_file = "semantic_net.html"
                    cli.net.export_html(html_file)
                    webbrowser.open(html_file)
                except Exception as e:
                    click.secho(f"Error generating visualization: {e}", fg="red")

            elif cmd == "help":
                print_help()

            else:
                click.secho("Unknown command. Type 'help' to see available commands.", fg="yellow")

        except KeyboardInterrupt:
            click.secho("\nGoodbye!", fg="cyan")
            break
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")

