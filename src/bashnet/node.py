class Node:
    def __init__(self, node_id: str, label:str, node_type: str, **attrs):
        if not all([node_id, label, node_type]):
            raise ValueError(f"Invalid Node: {node_id=} {label=} {node_type=}")
        self.id = node_id
        self.label = label
        self.type = node_type
        self.attrs = attrs

    def to_dict(self):
        return {
            "id": self.id,
            "label": self.label,
            "type": self.type,
            **self.attrs
        }
