import os
import json
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

    def simple_search(self, term: str) -> dict | None:
        node_id = self.net.get_node_id_by_label(term)
        if not node_id:
            return None
        return self.net.get_node(node_id)

    def deep_search(self, term: str) -> tuple[dict | None, dict]:
        node = self.simple_search(term)
        context: dict = {}

        if not node:
            context["fallback"] = self.net.search_relevant(term)
            return None, context

        node_id = node["id"]
        node_type = node.get("type")
        context: dict = {}

        if node_type == "command":
            context["options"] = [
                self.net.get_node(tid)
                for tid in self.net.get_neighbors_by_relation(node_id, "options")
                if self.net.get_node(tid)
            ]

        elif node_type == "concept":
            related = self.net.get_neighbors_with_relation(node_id)
            context["commands"] = [n for n in related.get("related", []) if isinstance(n, dict) and n["type"] == "command" and n["id"] != node_id]
            context["options"] = [n for n in related.get("related", []) if isinstance(n, dict) and n["type"] == "option" and n["id"] != node_id]
            context["others"] = [n for n in related.get("related", []) if isinstance(n, dict) and n["type"] not in ("command", "option") and n["id"] != node_id]

        elif node_type == "scripting":
            context["related"] = [
                n for n in self.net.get_neighbors_with_relation(node_id).get("related", [])
                if isinstance(n, dict) and n["id"] != node_id
            ]

        elif node_type == "option":
            context["commands"] = [
                self.net.get_node(source)
                for source in self.net.get_sources_by_relation(node_id, "options")
                if self.net.get_node(source)
            ]

        else:
            context["fallback"] = self.net.search_relevant(term)

        return node, context
