import json
from .semantic_net import SemanticNet
from .node import Node
from .edge import Edge


class JsonIO:
    def __init__(self, net: SemanticNet):
        self.net = net

    def load_entries(self, filepath: str) -> list[dict]:
        """Load and return all entries from a single JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def create_node(self, entry: dict):
        """Create a Node object from a dictionary entry and add it to the net."""
        if not isinstance(entry, dict) or not all(k in entry for k in ("id", "label", "type")):
            return
        node = Node(
            node_id=entry["id"],
            label=entry["label"],
            node_type=entry["type"],
            **{k: v for k, v in entry.items() if k not in {"id", "label", "type", "options", "related"}}
        )
        self.net.add_node(node)

    def create_edges(self, entry: dict):
        """Create edges for a given entry if the referenced nodes exist."""
        if not isinstance(entry, dict) or "id" not in entry:
            return
        for relation in ("options", "related"):
            for target in entry.get(relation, []):
                if self.net.has_node(target):
                    self.net.add_edge(Edge(source=entry["id"], target=target, relation=relation))
                else:
                    print(f"Warning: Target node '{target}' not found in net (source: {entry['id']})")

    def load_all(self, paths: list[str]):
        """Load all JSON files: first nodes, then edges."""
        all_entries: list[dict] = []
        for path in paths:
            all_entries.extend(self.load_entries(path))

        # Phase 1: Add all nodes
        for entry in all_entries:
            self.create_node(entry)

        # Phase 2: Add all edges
        for entry in all_entries:
            self.create_edges(entry)

    def export(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.net.to_dict(), f, indent=2, ensure_ascii=False)
