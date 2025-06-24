import networkx as nx
from .node import Node
from .edge import Edge

class SemanticNet:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node: Node):
        if not node.id or not node.label or not node.type:
            print(f"Warning: Skipping node with missing attributes: {node}")
            return
        self.graph.add_node(node.id, **node.to_dict())

    def add_edge(self, edge: Edge):
        self.graph.add_edge(edge.source, edge.target, relation=edge.relation)

    def get_node(self, node_id: str):
        return self.graph.nodes.get(node_id)

    def get_node_id_by_label(self, label: str) -> str | None:
        for node_id, attrs in self.graph.nodes(data=True):
            if attrs.get("label") == label:
                return node_id
        return None

    def get_neighbors(self, node_id: str):
        return list(self.graph.successors(node_id))

    def has_node(self, node_id: str) -> bool:
        return self.graph.has_node(node_id)

    def to_dict(self):
        return {
            "nodes": [
                {"id": n, **attrs}
                for n, attrs in self.graph.nodes(data=True)
                if isinstance(attrs, dict) and all(k in attrs for k in ("id", "label", "type"))
            ],
            "edges": [
                (u, v, d["relation"])
                for u, v, d in self.graph.edges(data=True)
            ]
        }
