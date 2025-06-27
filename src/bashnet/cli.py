import click
from .cli_core import BashnetCLI

def print_help():
    click.secho("Welcome to Bashnet CLI – Your semantic Bash learning tool!\n", fg="cyan")
    click.echo("Available commands:")
    click.echo("    import                      => Load all JSON files and rebuild the semantic net")
    click.echo("    search <term>               => Deep search: includes related concepts, options, examples")
    click.echo("    search <term> --simple      => Simple search: fast, shallow term match")
    click.echo("    help                        => Show this help again")
    click.echo("    exit                        => Exit the application")
    click.echo("    Press Ctrl+C anytime to exit.\n")

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
                cli.load_knowledge_net()
                cli.search(term, simple)
            elif cmd == "help":
                print_help()
            else:
                click.secho("Unknown command. Type 'help' to see available commands.", fg="yellow")

        except KeyboardInterrupt:
            click.secho("\nGoodbye!", fg="cyan")
            break
        except Exception as e:
            click.secho(f"Error: {e}", fg="red")


if __name__ == "__main__":
    main()
