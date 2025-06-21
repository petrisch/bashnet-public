import networkx as nx
from .node import Node
from .edge import Edge

class SemanticNet:
    def __init__(self):
        self.graph = nx.DiGraph()

    def add_node(self, node: Node):
        self.graph.add_node(node.id, **node.to_dict())
    
    def add_edge(self, edge: Edge):
        self.graph.add_edge(edge.source, edge.target, relation = edge.relation)

    def get_node(self, node_id: str):
        return self.graph.nodes.get(node_id)
    
    def get_neighbors(self, node_id: str):
        return list(self.graph.successors(node_id))
    
    def to_dict(self):
        return {
            "nodes": [self.graph.nodes[n] for n in self.graph.nodes],
            "edges": [(u, v, d["relation"]) for u, v, d in self.graph.edges(data=True)]
        }