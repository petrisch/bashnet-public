import click

def print_node_info(node: dict):
    """Formatted display of a single node's information."""
    click.secho(f"\nTerm found: {node.get('label')} ({node.get('type')})", fg="green")

    if "description" in node:
        click.secho(f"\nDescription: {node['description']}", fg="blue")

    if "category" in node:
        click.secho(f"\nCategory: {node['category']}", fg="blue")

    if "tags" in node:
        tags = ', '.join(node.get("tags", []))
        click.secho(f"\nTags: {tags}", fg="blue")

    examples = node.get("examples")
    if examples:
        click.secho("\nUsage Examples:", fg="blue")
        if isinstance(examples[0], dict):
            for example in examples:
                cmd = example.get("command", "")
                out = example.get("expected_output", "").strip()
                expl = example.get("explanation", "")
                if "\n" in out:
                    formatted_out = "\n    " + out.replace("\n", "\n    ")
                    click.echo(f"  Command: {cmd}")
                    click.echo(f"  Output:{formatted_out}")
                else:
                    click.echo(f"  Command: {cmd}")
                    click.echo(f"  Output:  {out}")
                click.echo(f"  Note:    {expl}\n")
        else:
            for entry in examples:
                click.echo(f"{entry}")

    links = node.get("links")
    if links:
        click.secho("\nLinks:", fg="blue")
        for url in links:
            click.echo(f"{url}")


def print_context_for_command(context: dict):
    options = context.get("options", [])
    if options:
        click.secho("\nUsable Options:", fg="blue")
        for opt in options:
            if isinstance(opt, dict):
                click.echo(f"=> {opt['label']}: {opt.get('description', 'No description')}")


def print_context_for_concept(context: dict):
    cmds = context.get("commands", [])
    opts = context.get("options", [])
    others = context.get("others", [])

    if cmds:
        click.secho("\nRelated Commands:", fg="blue")
        for c in cmds:
            if isinstance(c, dict):
                click.echo(f"=> {c['label']}: {c.get('description', 'No description')}")

    if opts:
        click.secho("\nAssociated Options:", fg="blue")
        for o in opts:
            if isinstance(o, dict):
                click.echo(f"=> {o['label']}: {o.get('description', 'No description')}")

    if others:
        click.secho("\nOther Relations:", fg="blue")
        for o in others:
            if isinstance(o, dict):
                click.echo(f"=> {o['label']} ({o['type']})")


def print_context_for_scripting(context: dict):
    related = context.get("related", [])
    if related:
        click.secho("\nRelated Concepts:", fg="blue")
        for r in related:
            if isinstance(r, dict):
                click.echo(f"=> {r['label']}: {r.get('description', 'No description')}")


def print_context_for_option(context: dict):
    used_by = context.get("commands", [])
    if used_by:
        click.secho("\nUsed in Commands:", fg="blue")
        for c in used_by:
            if isinstance(c, dict):
                click.echo(f"=> {c['label']}: {c.get('description', 'No description')}")


def print_context_fallback(context: dict):
    if context.get("fallback"):
        click.secho("\nRelated matches (by relevance):", fg="magenta")
        for rel, score in context["fallback"]:
            if isinstance(rel, dict):
                click.echo(f"=> {rel['label']} ({rel['type']}) [score: {score}]")
                if rel.get("description"):
                    click.echo(f"  Description: {rel['description']}")
                    click.echo("")


def print_deep_search_context(node: dict, context: dict):
    """Delegates output rendering to type-specific handlers."""
    t = node.get("type")

    if t == "command":
        print_context_for_command(context)
    elif t == "concept":
        print_context_for_concept(context)
    elif t == "scripting":
        print_context_for_scripting(context)
    elif t == "option":
        print_context_for_option(context)

    print_context_fallback(context)
