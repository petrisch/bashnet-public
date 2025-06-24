import json
from .semantic_net import SemanticNet
from .node import Node
from .edge import Edge

class JsonIO:
    def __init__(self, net: SemanticNet):
        self.net = net
    
    def load_file(self, filepath: str):
        with open(filepath, "r", encoding="utf-8") as f:
            items = json.load(f)

        # Create all Nodes
        for entry in items:
            if not isinstance(entry, dict) or not all(k in entry for k in ("id", "label", "type")):
                continue
            node = Node(
                node_id=entry["id"],
                label=entry["label"],
                node_type=entry["type"],
                **{k: v for k, v in entry.items() if k not in {"id", "label", "type", "examples", "options", "related", "links"}}
            )
            self.net.add_node(node)

        # Create all Edges
        for entry in items:
            if not isinstance(entry, dict) or "id" not in entry:
                continue
            for relation in ("options", "related"):
                for target in entry.get(relation, []):
                    if self.net.has_node(target):  
                        self.net.add_edge(Edge(source=entry["id"], target=target, relation=relation))
                    else:
                        print(f"Warning: Target node '{target}' not found in net (source: {entry['id']})")


    def load_all(self, paths: list[str]):
        for path in paths:
            self.load_file(path)

    def export(self, filepath: str):
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(self.net.to_dict(), f, indent=2, ensure_ascii=False)
