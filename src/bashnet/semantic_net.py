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

    def has_node(self, node_id: str) -> bool:
        return self.graph.has_node(node_id)

    def get_neighbors_with_relation(self, node_id: str) -> dict[str, list[dict]]:
        result: dict[str, list[dict]] = {}
        for target_id in self.graph.successors(node_id):
            if target_id == node_id:
                continue
            relation = self.graph.edges[node_id, target_id]["relation"]
            result.setdefault(relation, []).append(self.graph.nodes[target_id])
        return result

    def get_neighbors_by_relation(self, node_id: str, relation: str) -> list[str]:
        return [
            target for target in self.graph.successors(node_id)
            if self.graph.edges[node_id, target]["relation"] == relation and target != node_id
        ]

    def get_sources_by_relation(self, target_id: str, relation: str) -> list[str]:
        return [
            source for source in self.graph.predecessors(target_id)
            if self.graph.edges[source, target_id]["relation"] == relation and source != target_id
        ]

    def search_relevant(self, term: str) -> list[tuple[dict, int]]:
        results: list[tuple[dict, int]] = []
        term_lower = term.lower()

        for node_id, attrs in self.graph.nodes(data=True):
            score = 0
            if term_lower in attrs.get("label", "").lower():
                score += 3
            if any(term_lower in tag.lower() for tag in attrs.get("tags", [])):
                score += 2
            if term_lower in attrs.get("description", "").lower():
                score += 1
            if term_lower in attrs.get("category", "").lower():
                score += 1
            if any(term_lower in str(ex).lower() for ex in attrs.get("examples", [])):
                score += 1
            if score > 0:
                results.append((attrs, score))

        return sorted(results, key=lambda x: -x[1])

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
