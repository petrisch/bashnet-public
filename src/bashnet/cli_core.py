import os
import json
import click
from .semantic_net import SemanticNet
from .node import Node
from .edge import Edge
from .json_io import JsonIO

class BashnetCLI:
    def __init__(self):
        self.data_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data"))
        self.knowledge_file = os.path.join(self.data_dir, "knowledge_net.json")
        self.net = SemanticNet()

    def load_knowledge_net(self):
        if not os.path.exists(self.knowledge_file):
            raise FileNotFoundError("knowledge_net.json not found. Please run the import command first.")
        with open(self.knowledge_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            for node in data["nodes"]:
                self.net.add_node(Node(
                    node_id=node["id"],
                    label=node["label"],
                    node_type=node["type"],
                    **{k: v for k, v in node.items() if k not in {"id", "label", "type"}}
                ))
            for source, target, relation in data["edges"]:
                self.net.add_edge(Edge(source, target, relation))

    def import_data(self):
        loader = JsonIO(self.net)
        files = [
            os.path.join(self.data_dir, "commands.json"),
            os.path.join(self.data_dir, "options.json"),
            os.path.join(self.data_dir, "concepts.json"),
            os.path.join(self.data_dir, "scripting.json"),
        ]
        loader.load_all(files)
        loader.export(self.knowledge_file)
        click.secho(f"Imported and saved network to: {self.knowledge_file}", fg="green")

    def search(self, term: str, simple: bool):
        node_id = self.net.get_node_id_by_label(term)
        if not node_id:
            click.secho(f"Error: Term '{term}' not found.", fg="red")
            return

        node = self.net.get_node(node_id)
        click.secho(f"\nTerm found: {node['label']} ({node['type']})", fg="green")

        if not simple:
            neighbors = self.net.get_neighbors(node_id)
            if neighbors:
                click.echo("Related concepts:")
                for nid in neighbors:
                    info = self.net.get_node(nid)
                    click.echo(f"- {info['label']} ({info['type']})")
