import click

def print_node_info(node: dict):
        """Nicely format and print node attributes from the semantic net."""
        click.secho(f"\nTerm found: {node.get('label')} ({node.get('type')})", fg="green")

        if "description" in node:
            click.secho(f"\nDescription: {node['description']}", fg="blue")
        
        if "category" in node:
            click.secho(f"\nCategory: {node['category']}", fg="blue")
        
        if "tags" in node:
            click.secho(f"\nTags: {', '.join(node['tags'])}", fg="blue")
        
        if "examples" in node and node["examples"]:
            click.secho("\nUsage Examples:", fg="blue")
            for example in node["examples"]:
                cmd = example.get("command", "")
                out = example.get("expected_output", "")
                expl = example.get("explanation", "")
                click.echo(f"- Command: {cmd}")
                click.echo(f"  Output: {out}")
                click.echo(f"  Note: {expl}\n")
        
        if "links" in node and node["links"]:
            click.secho("\nLinks:", fg="blue")
            for url in node["links"]:
                click.echo(f"- {url}")